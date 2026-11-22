from classes.StockMovementClass import StockMovementClass

class StockMovementProcess:
    def __init__(self):
        self.movement_class = StockMovementClass()

    def execute_transfer(self, sku_id: int, from_location_id: int, to_location_id: int, quantity: int) -> int:
        # cannot move to the exact same location
        if from_location_id == to_location_id:
            raise ValueError("source location and destination location cannot be the same")

        # quantity must be strictly positive
        if quantity <= 0:
            raise ValueError("quantity to transfer must be greater than zero")

        return self.movement_class.transfer_stock(sku_id, from_location_id, to_location_id, quantity)

    def get_movement_history(self, sku_id: int = None):
        return self.movement_class.get_movements(sku_id)