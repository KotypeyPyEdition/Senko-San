import discord
import random
from classes import item
import requests
import config
import json


class DBUtils:
    def __init__(self, bot, path=None):
        self.bot = bot
        self.shop_path = 'data/shop.json'
        self.guild_config = 'data/guild_config.json'
        self.guild_shop = 'data/guild_shop.json'
        if path is None:
            self.path = "data/users.json"

    def get_item_data(self, itemid):
        with open(self.shop_path) as f:
            file = json.load(f)
            for i in file['shop']:
                if i['id'] == itemid:
                    return i
    def get_user_inventory_list(self, userid):
        userid = str(userid)
        """
        # Old code
        res = await self.db.execute('SELECT * FROM `inv` WHERE owner_id = {}'.format(user))
        items = []
        for i in res:
            items.append(item.item(i[1]))
        self.disconnect(db)"""
        items = []
        with open(self.path) as f:
            file = json.load(f)
            temp = file[userid]['inv']
            for i in temp:
                l.append(item.item(i))

        return l

    def create_user_inventory(self, user):
        pass

    def add_item(self, userid, itm, count=1):
        """
        # Old code
        await self.db.execute(
            'INSERT INTO `inv`(`owner_id`, `item_id`, `count`) VALUES ({},{},{})'.format(userid, itm, count))
        """
        userid = str(userid)
        with open(self.path) as f:  # Loading all users from file by path
            file = json.load(f)

            file[userid]['inv'] = file[userid]['inv'].append(itm)

        with open(self.path, 'w') as sf:  # Writing all users to file by path
            json.dump(file, sf)

    async def get_shop_list(self):
        """
        # Old code
        res = await self.db.execute('SELECT * FROM items')
        l = []
        for i in res:
            ia = item.item(i[0])
            l.append(str(ia))
        """

        l = None

        return l

    async def get_user_top_raw(self):
        top = []
        with open(self.path) as file:
            file = json.load(f)

            for i in file:
                top.append(file[i])

        return top
            

    def create_user_profile(self, id):
        id = str(id)
        

        with open(self.path) as f:
            file = json.load(f)
            try:
                if file[id]:
                    return
            except Exception as e:

                    file[id] = {'level': 1, 'xp': 0, 'gold': 0, 'inv': []}
                    with open('data/users.json', 'w') as data:
                        json.dump(file, data)


    def get_user_leveling(self, userid):
        userid = str(userid)
        inf = {}
        with open(self.path) as f:
            d = json.load(f)
            inf['level'] = d[userid]['level']
            inf['xp'] = d[userid]['xp']
            inf['gold'] = d[userid]['gold']
        return inf

    def add_exp(self, userid, count: int):
        userid = str(userid)
        with open(self.path) as f:
            file = json.load(f)
            
            file[userid]['xp'] += file[userid]['xp'] + count
        with open(self.path, 'w') as data:
            json.dump(file, data)


    def add_gold(self, userid, count: int):
        userid = str(userid)
        with open(self.path) as f:
            file = json.load(f)
            
            file[userid]['gold'] = file[userid]['gold'] + count
        with open(self.path, 'w') as data:
            json.dump(file, data)



    def level_up(self, userid):
        userid = str(userid)
        with open(self.path) as f:
            file = json.load(f)
            
            file[userid]['level'] += 1
            file[userid]['xp'] = 0
        with open(self.path, 'w') as data:
            json.dump(file, data)

    """
    Social fish .-.
    """

    async def create_user_socail_profile(self, user: discord.User):
        res = await self.db.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        if len(res) == 0:
            await self.db.execute(
                f"INSERT INTO `user_info` (`user_id`, `description`) VALUES ({user.id},\"Not provided\")")


        else:
            return

    async def edit_desc(self, user: discord.User, description: str):
        await self.db.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        if (len(res) == 0):
            raise Exception("This user is not exits!")

        await self.db.execute(
            'UPDATE `user_info` SET `description`=\"{}\" WHERE user_id={}'.format(description, user.id))

    async def get_user_desc(self, user: discord.User):

        res = await self.db.execute('SELECT description FROM user_info WHERE user_id={}'.format(user.id))
        return res[0][0]

    """
    Osu! module
    """

    async def create_profile(self, user: discord.User, osu_name: str):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        if (len(res) != 0):
            raise Exception('You already setuped Lol')
        r = requests.get(f'https://osu.ppy.sh/api/get_user?k={config.osu_token}&u={osu_name}')
        r = r.json()[0]
        osu_id = r['user_id']
        q = 'INSERT INTO `user_keys`(`user_id`, `server_user_id`) VALUES ({},"{}")'.format(user.id, osu_id)
        await self.db.execute(q)

    async def user_profile_exits(self, user: discord.User):
        query = 'SELECT * FROM user_keys WHERE user_id={}'.format(user.id)
        res = await self.db.execute(query)
        if (len(res) == 0):
            return False
        else:
            return True

    async def get_profile(self, user: discord.User):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        if (len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': user.id, 'osu_id': res[0][1]}

            return inf

    async def get_profile_id(self, userid):
        res = await self.db.execute('SELECT * FROM user_keys WHERE user_id={}'.format(userid))
        if (len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': userid, 'osu_id': res[0][1]}

            return inf

    def set_lvlup_msg(self, guild: discord.Guild, state):
        gid = str(guild.id)

        with open(self.guild_config) as f:
            file = json.load(f)
            file[gid]['lvl_msg_enabled'] = state
        with open(self.guild_config, 'w') as data:
            json.dump(file, data)




    def register_guild_config(self, guild: discord.Guild):
        gid = str(guild.id)
        with open(self.guild_config) as f:
            file = json.load(f)
            try:
                a = file[gid]['lvl_msg_enabled']
            except Exception as e:
                file[gid] = {'lvl_msg_enabled': 1}
        with open(self.guild_config, 'w') as data:
            json.dump(file, data)

    def get_guild_config(self, guild: discord.Guild):
        gid = str(guild.id)
        with open(self.guild_config) as f:
            file = json.load(f)
            return file[gid]

    def all_users(self):
        with open(self.path) as f:
            data = json.load(f)
        return data
    def register_guild_shop(self, guild: discord.Guild):
        gid = str(guild.id)
        with open(self.guild_shop) as f:
            file = json.load(f)
            try:
                a = file[gid][0]
            except:
                file[gid] = []

        with open(self.guild_shop, 'w') as data:
            json.dump(file, data)
    


    def get_role_shop(self, guild: discord.Guild):
        gid = str(guild.id)
        with open(self.guild_shop) as f:
            file = json.load(f)

        return file[gid]
    

    def add_shop_role(self,guild: discord.Guild, role: discord.Role, cost):
        gid = str(guild.id)
        with open(self.guild_shop) as f:
            file = json.load(f)
        file[gid].append({"role": role.id, "cost": cost})
        with open(self.guild_shop, 'w') as data:
            json.dump(file, data)


    def remove_shop_role(self,guild: discord.Guild, role: discord.Role):
        gid = str(guild.id)
        with open(self.guild_shop) as f:
            file = json.load(f)
        shop = file[gid]
        counter = 0
        for i in shop:
            if i['role'] == role.id:
                del file[gid][counter]
                break
            counter += 1
        with open(self.guild_shop, 'w') as data:
            json.dump(file, data)
        
