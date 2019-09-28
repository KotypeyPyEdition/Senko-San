import utils.database as ub

class item:
    def __init__(self, tid, bot):
        self.id = tid
        self.db = ub.DBUtils()
        self.execute('SELECT * FROM `items` WHERE item_id = {}'.format(self.id))
        self.dict = cursor.fetchall()[0]
        self.title = self.dict[1]
        self.cost = self.dict[2]
        self.power = self.dict[3]


    def dict_(self):
        return self.dict

    def __str__(self):
        return f"title: {self.title}, cost: {self.cost}, power: {self.power}, id: {self.id}"

    
