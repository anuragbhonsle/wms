from flask import Blueprint, jsonify, request

from classes.InwardClass import RelatedRecordNotFound
from classes.master_data import MasterData
from processes.InwardProcess import InwardProcess

api_bp = Blueprint("api", __name__)
master_data = MasterData()
inward_process = InwardProcess()


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
