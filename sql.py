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
# stock movement queries

CHECK_SKU_EXISTS = """
    SELECT id FROM skus WHERE id = %s
"""

CHECK_LOCATION_ACTIVE ="""
    SELECT id, is_active FROM locations WHERE id = %s
"""
# FOR UPDATE to force sequential updates means first request locks the row second request will have to wait for commit or rollback
GET_SOURCE_INVENTORY_FOR_UPDATE = """
    SELECT id, quantity FROM inventory WHERE sku_id = %s and location_id = %s FOR UPDATE
"""

DEDUCT_SOURCE_INVENTORY = """
    UPDATE inventory SET quantity = quantity - %s WHERE sku_id = %s AND location_id = %s
"""

UPSERT_DESTINATION_INVENTORY = """
    INSERT INTO inventory(sku_id,location_id,quantity) VALUES(%s,%s,%s)
    ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
"""

CREATE_STOCK_MOVEMENT = """
    INSERT INTO stock_movement_items(sku_id, from_location_id, to_location_id, quantity)
    VALUES(%s, %s, %s, %s)
"""

GET_STOCK_MOVEMENTS = """
    SELECT
    smi.id
    ,smi.sku_id
    ,s.sku_code
    ,smi.from_location_id
    ,fl.location_code AS from_location_code
    ,smi.to_location_id
    ,tl.location_code AS to_location_code
    ,smi.quantity
    ,smi.created_at
    FROM stock_movement_items smi
    INNER JOIN skus s ON smi.sku_id = s.id
    INNER JOIN locations fl ON smi.from_location_id = fl.id
    INNER JOIN locations tl ON smi.to_location_id = tl.id
    ORDER BY smi.created_at DESC
"""

GET_STOCK_MOVEMENTS_BY_SKU = """
    SELECT
    smi.id
    ,smi.sku_id
    ,s.sku_code
    ,smi.from_location_id
    ,fl.location_code AS from_location_code
    ,smi.to_location_id
    ,tl.location_code AS to_location_code
    ,smi.quantity
    ,smi.created_at
    FROM stock_movement_items smi
    INNER JOIN skus s ON smi.sku_id = s.id
    INNER JOIN locations fl ON smi.from_location_id = fl.id
    INNER JOIN locations tl ON smi.to_location_id = tl.id
    WHERE smi.sku_id = %s
    ORDER BY smi.created_at DESC
"""

GET_ALL_INVENTORY = """
    SELECT 
    i.id AS stock_id
    ,i.sku_id
    ,s.sku_code
    ,s.description AS sku_description
    ,i.location_id
    ,l.location_code
    ,lt.type_name AS location_type
    ,lt.is_pickable
    ,i.quantity
    FROM inventory i
    JOIN skus s ON i.sku_id = s.id
    JOIN locations l ON i.location_id = l.id
    JOIN location_types lt ON l.location_type_id = lt.id
    WHERE i.quantity > 0
    ORDER BY s.sku_code, l.location_code
"""
GET_INVENTORY_BY_SKU = """
    SELECT 
    i.id AS stock_id
    ,i.sku_id
    ,s.sku_code
    ,s.description AS sku_description
    ,i.location_id
    ,l.location_code
    ,lt.type_name AS location_type
    ,lt.is_pickable
    ,i.quantity
    FROM inventory i
    JOIN skus s ON i.sku_id = s.id
    JOIN locations l ON i.location_id = l.id
    JOIN location_types lt ON l.location_type_id = lt.id
    WHERE i.sku_id = %s AND i.quantity > 0
    ORDER BY l.location_code
"""
GET_INVENTORY_BY_LOCATION = """
    SELECT 
        l.id AS location_id
        ,l.location_code
        ,lt.type_name AS location_type
        ,lt.is_pickable
        ,i.sku_id
        ,s.sku_code
        ,s.description AS sku_description
        ,COALESCE(i.quantity, 0) AS quantity
    FROM locations l
    JOIN location_types lt ON l.location_type_id = lt.id
    LEFT JOIN inventory i ON l.id = i.location_id AND i.quantity > 0
    LEFT JOIN skus s ON i.sku_id = s.id
    WHERE l.id = %s
"""