
import discord
import random
from classes import item
import requests
import config
import json
class DBUtils:
    def __init__(self, bot):
        self.bot = bot

    async def get_user_inventory_list(self, user):

        res = await self.db.execute('SELECT * FROM `inv` WHERE owner_id = {}'.format(user))
        items = []
        for i in res:
            items.append(item.item(i[1]))
        self.disconnect(db)
        return items

    def create_user_inventory(self, user):
        pass

    async def add_item(self, userid, itm, count=1):
        await self.db.execute('INSERT INTO `inv`(`owner_id`, `item_id`, `count`) VALUES ({},{},{})'.format(userid, itm, count))


    async def get_shop_list(self):
        res = await self.db.execute('SELECT * FROM items')
        l = []
        for i in res:
            ia = item.item(i[0])
            l.append(str(ia))
        return l 



    async def get_user_top_raw(self):
        rd = await self.db.execute('SELECT * FROM user_leveling')
        r = {}
        ind = 0
        for i in len(rd) - 1:
            r[rd[ind]] = rd[2]
        return r
    

    def create_user_profile(self, id):
        id = str(id)
        with json.load(open('data/users.json', 'r')) as data:
            if data[id]:
                return
            else:
                data[id] = {'level': 1, 'xp': 0, 'gold': 0}
        with json.load(open('data/users.json', 'rb+')) as data1:
            json.dumps(data)


    def get_user_leveling(self, user: discord.User):
        inf = {}
        with json.load(open('data/users.json', 'r')) as d:


            inf['level'] = d['level']
            inf['xp'] = d['xp']
            inf['gold'] = d['gold']
        return inf




    async def add_exp(self, user: discord.User, count: int):
        res = await self.db.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        if(len(res) == 0):
            raise Exception("This user is not exits!")

        mapa = await self.get_user_leveling(user)

        await self.db.execute('UPDATE `user_leveling` SET `level`={},`xp`={} WHERE user_id={}'.format(mapa['level'], mapa['xp'] + count, mapa['user_id']))


    async def remove_gold(self, user: discord.User, count: int):
        res = self.db.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        if(len(res) == 0):
            raise Exception("This user is not exits!")
        mapa = await self.get_user_leveling(user)
        await self.db.execute('UPDATE `user_leveling` SET`gold`={} WHERE user_id = {}'.format(mapa['gold'] - count, user.id))

        
    async def add_gold(self, user: discord.User, count: int):
        res = await self.db.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        if(len(res) == 0):
            raise Exception("This user is not exits!")

        mapa = await self.get_user_leveling(user)

        await self.db.execute('UPDATE `user_leveling` SET `gold`={} WHERE user_id={}'.format(mapa['gold'] + random.randrange(101), mapa['user_id']))




    async def level_up(self, user: discord.User):
        res = self.db.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        if(len(res) == 0):
            raise Exception("This user is not exits!")



        mapa = await self.get_user_leveling(user)

        await self.db.execute('UPDATE `user_leveling` SET `level`={},`xp`={} WHERE user_id={}'.format(mapa['level'] + 1, 0, mapa['user_id']))
    """
    Social fish .-.
    """

    async def create_user_socail_profile(self, user: discord.User):
        res = await self.db.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        if len(res) == 0:
            await self.db.execute(f"INSERT INTO `user_info` (`user_id`, `description`) VALUES ({user.id},\"Not provided\")")
        

        else:
            return

    async def edit_desc(self, user: discord.User, description: str):
        await self.db.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        if(len(res) == 0):
            raise Exception("This user is not exits!")

        await self.db.execute('UPDATE `user_info` SET `description`=\"{}\" WHERE user_id={}'.format(description, user.id))

    async def get_user_desc(self, user: discord.User):
        
        res = await self.db.execute('SELECT description FROM user_info WHERE user_id={}'.format(user.id))
        return res[0][0]



    """
    Osu! module
    """

    async def create_profile(self, user: discord.User, osu_name: str):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        if(len(res) != 0):
            raise Exception('You already setuped Lol')
        r = requests.get(f'https://osu.ppy.sh/api/get_user?k={config.osu_token}&u={osu_name}')
        r = r.json()[0]
        osu_id = r['user_id']
        q = 'INSERT INTO `user_keys`(`user_id`, `server_user_id`) VALUES ({},"{}")'.format(user.id, osu_id)
        await self.db.execute(q)



    async def user_profile_exits(self, user: discord.User):
        query = 'SELECT * FROM user_keys WHERE user_id={}'.format(user.id)
        res = await self.db.execute(query)
        if(len(res) == 0):
            return False
        else:
            return True

    async def get_profile(self, user: discord.User):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        if(len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': user.id,'osu_id':res[0][1]}
            
            return inf

    async def get_profile_id(self, userid):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(userid))
        if(len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': userid,'osu_id':res[0][1]}
            
            return inf
            

    



        

        

    
