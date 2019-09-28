from utils import database

class Clan:
    def __init__(self, id):
        self.id = id
        self.info = database.DButils().connect()