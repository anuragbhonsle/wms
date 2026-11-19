import sql
from db import fetch_all, get_db_connection


class RelatedRecordNotFound(Exception):
    pass


class InwardClass:
    def get_all(self):
        return fetch_all(sql.GET_INWARDS)

    def create(self, po_id, user_id, status_id):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(sql.GET_PURCHASE_ORDER_BY_ID, (po_id,))
                if cursor.fetchone() is None:
                    raise RelatedRecordNotFound("Purchase order not found")

                cursor.execute(sql.GET_USER_BY_ID, (user_id,))
                if cursor.fetchone() is None:
                    raise RelatedRecordNotFound("User not found")

                cursor.execute(sql.GET_STATUS_BY_ID, (status_id,))
                if cursor.fetchone() is None:
                    raise RelatedRecordNotFound("Status not found")

                cursor.execute(sql.CREATE_INWARD, (po_id, user_id, status_id))
                connection.commit()
                return cursor.lastrowid
            finally:
                cursor.close()
        finally:
            connection.close()
