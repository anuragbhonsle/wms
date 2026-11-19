GET_SELLERS = "SELECT * FROM sellers"
GET_SKUS = "SELECT * FROM skus"

GET_PURCHASE_ORDERS = """
    SELECT * FROM purchase_orders
"""

GET_PURCHASE_ORDER_BY_ID = """
    SELECT * FROM purchase_orders
    WHERE id = %s
"""

CREATE_PURCHASE_ORDER = """
    INSERT INTO purchase_orders (seller_id, po_date)
    VALUES (%s, %s)
"""

CREATE_PURCHASE_ORDER_ITEM = """
    INSERT INTO purchase_order_items (po_id, sku_id, quantity)
    VALUES (%s, %s, %s)
"""

GET_INWARDS = """
    SELECT * FROM inwards
"""

GET_USER_BY_ID = """
    SELECT id FROM users
    WHERE id = %s
"""

GET_STATUS_BY_ID = """
    SELECT id FROM statuses
    WHERE id = %s
"""

CREATE_INWARD = """
    INSERT INTO inwards (po_id, user_id, status_id)
    VALUES (%s, %s, %s)
"""

CREATE_INWARD_ITEM = """
    INSERT INTO inward_items
    (inward_id, po_item_id, received_qty, sellable_qty, non_sellable_qty)
    VALUES (%s, %s, %s, %s, %s)
"""

CREATE_PUTAWAY_TASK = """
    INSERT INTO putaway_tasks
    (inward_item_id, location_id, quantity, task_status, stock_status)
    VALUES (%s, %s, %s, %s, %s)
"""
