from flask import Blueprint, jsonify, request
from classes.InwardClass import RelatedRecordNotFound
from classes.master_data import MasterData
from processes.InwardProcess import InwardProcess
from classes.StockMovementClass import (
    InsufficientStockError,
    InvalidLocationError,
    SkuNotFoundError,
)
from processes.StockMovementProcess import StockMovementProcess

api_bp = Blueprint("api", __name__)
master_data = MasterData()
inward_process = InwardProcess()
stock_movement_process = StockMovementProcess()

@api_bp.route("/")
def home():
    return "Warehouse Management System"

@api_bp.route("/api/sellers", methods=["GET"])
def get_sellers():
    return jsonify(master_data.get_all_sellers())

@api_bp.route("/api/skus", methods=["GET"])
def get_skus():
    return jsonify(master_data.get_all_skus())

@api_bp.route("/api/inwards/", methods=["GET"])
def get_inwards():
    return jsonify(inward_process.get_inwards())

@api_bp.route("/api/inwards/", methods=["POST"])
def create_inward():
    data = request.get_json()
    required_fields = ("po_id", "user_id", "status_id")

    if not isinstance(data, dict) or any(field not in data for field in required_fields):
        return jsonify({"error": "po_id, user_id, and status_id are required"}), 400

    values = [data[field] for field in required_fields]
    if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in values):
        return jsonify({"error": "po_id, user_id, and status_id must be positive integers"}), 400

    try:
        inward_id = inward_process.create_inward(*values)
    except RelatedRecordNotFound as error:
        return jsonify({"error": str(error)}), 404

    return jsonify({
        "id": inward_id,
        "po_id": data["po_id"],
        "user_id": data["user_id"],
        "status_id": data["status_id"],
    }), 201

@api_bp.route("/api/stock-movements", methods=["POST"])
def transfer_stock():
    data = request.get_json()
    required_fields = ("sku_id", "from_location_id", "to_location_id", "quantity")
    if not isinstance(data, dict) or any(field not in data for field in required_fields):
        return jsonify({"error": f"Required fields: {', '.join(required_fields)}"}), 400
    values = [data[f] for f in required_fields]
    # ensure all values are positive integers
    if any(not isinstance(v, int) or isinstance(v, bool) or v <= 0 for v in values):
        return jsonify({"error": "sku_id, from_location_id, to_location_id, and quantity must be positive integers"}), 400
    try:
        movement_id = stock_movement_process.execute_transfer(
            sku_id=data["sku_id"],
            from_location_id=data["from_location_id"],
            to_location_id=data["to_location_id"],
            quantity=data["quantity"],
        )
        return jsonify({
            "message": "Stock relocated successfully",
            "data": {
                "movement_item_id": movement_id,
                "sku_id": data["sku_id"],
                "from_location_id": data["from_location_id"],
                "to_location_id": data["to_location_id"],
                "transferred_quantity": data["quantity"],
            }
        }), 201

    except (ValueError, InsufficientStockError) as err:
        return jsonify({"error": str(err)}), 400
    except (InvalidLocationError, SkuNotFoundError) as err:
        return jsonify({"error": str(err)}), 404
    except Exception as err:
        return jsonify({"error": "Internal server error", "details": str(err)}), 500
    
@api_bp.route("/api/stock-movements", methods=["GET"])
def get_stock_movements():
    sku_id = request.args.get("sku_id", type=int)
    movements = stock_movement_process.get_movement_history(sku_id=sku_id)
    return jsonify({"data": movements}), 200