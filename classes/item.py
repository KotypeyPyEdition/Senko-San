import utils.database as ub

class item:
    def __init__(self, tid, bot):
        self.id = tid
        self.db = ub.DBUtils(bot)
        self.dict = self.db.get_item_data(self.id)
        self.title = self.dict['title']
        self.cost = self.dict['cost']
        self.power = self.dict['power']


    def dict_(self):
        return self.dict

    def __str__(self):
        return f"title: {self.title}, cost: {self.cost}, power: {self.power}, id: {self.id}"

    
