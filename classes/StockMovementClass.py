import sql 
from db import get_db_connection

class InsufficientStockError(Exception):
    pass

class InvalidLocationError(Exception):
    pass

class SkuNotFoundError(Exception):
    pass

class StockMovementClass:
    def transfer_stock(self,sku_id: int,from_location_id: int, to_location_id: int, quantity: int) -> int:
        connection = get_db_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            try:
                # verify that sku exists
                cursor.execute(sql.CHECK_SKU_EXISTS,(sku_id,))
                if cursor.fetchone() is None:
                    raise SkuNotFoundError(f"SKU ID {sku_id} does not exist")

                # verify if from_location exists & is active
                cursor.execute(sql.CHECK_LOCATION_ACTIVE, (from_location_id,))
                from_loc = cursor.fetchone()
                if not from_loc:
                    raise InvalidLocationError(f"Source location {from_location_id} does not exist")
                if not from_loc["is_active"]:
                    raise InvalidLocationError(f"Source location {from_location_id} is inactive")

                # verify if to_Location exists and is active
                cursor.execute(sql.CHECK_LOCATION_ACTIVE, (to_location_id,))
                to_loc = cursor.fetchone()
                if not to_loc:
                    raise InvalidLocationError(f"Destination location {to_location_id} does not exist")
                if not to_loc["is_active"]:
                    raise InvalidLocationError(f"Destination location {to_location_id} is inactive")

                # get source inventory for update
                cursor.execute(sql.GET_SOURCE_INVENTORY_FOR_UPDATE, (sku_id, from_location_id))
                source_row = cursor.fetchone()
                available_qty = source_row["quantity"] if source_row else 0
                if available_qty < quantity:
                    raise InsufficientStockError(
                        f"Insufficient stock in source location {from_location_id}. "
                        f"Available: {available_qty}, Requested: {quantity}."
                    )

                #deduct from source
                cursor.execute (sql.DEDUCT_SOURCE_INVENTORY,(quantity, sku_id, from_location_id))

                # add to destination
                cursor.execute(sql.UPSERT_DESTINATION_INVENTORY, (sku_id, to_location_id, quantity))

                #record log
                cursor.execute(
                    sql.CREATE_STOCK_MOVEMENT,
                    (sku_id, from_location_id, to_location_id, quantity)
                )
                movement_id = cursor.lastrowid

                #commit transaction
                connection.commit()
                return movement_id

            except Exception:
                connection.rollback()
                raise

            finally: cursor.close()

        finally: connection.close()

    def get_movements(self, sku_id: int = None):
        # fetches movement logs
        connection = get_db_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            try:
                if sku_id:
                    cursor.execute(sql.GET_STOCK_MOVEMENTS_BY_SKU, (sku_id,))
                else:
                    cursor.execute(sql.GET_STOCK_MOVEMENTS)
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            connection.close()