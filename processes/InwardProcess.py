from classes.InwardClass import InwardClass

class InwardProcess:
    def __init__(self):
        self.inward = InwardClass()

    def get_inwards(self):
        return self.inward.get_all()

    def create_inward(self, po_id, user_id, status_id):
        return self.inward.create(po_id, user_id, status_id)
