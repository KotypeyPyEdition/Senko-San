import mysql.connector
import discord
import random
from classes import item
import requests
import config
class DBUtils:
    def __init__(self):
        self.host=config.mysql_host
        self.user=config.mysql_user
        self.passwd=config.mysql_password
        self.database=config.mysql_database
        


    def connect(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database)
        return db, db.cursor()

    def disconnect(self, db):
        db.close()
        cursor = None
    def get_user_inventory_list(self, user):

        db, cursor = self.connect()
        cursor.execute('SELECT * FROM `inv` WHERE owner_id = {}'.format(user))
        res = cursor.fetchall()
        items = []
        for i in res:
            items.append(item.item(i[1]))
        self.disconnect(db)
        return items

    def create_user_inventory(self, user):
        pass

    def add_item(self, userid, itm, count=1):
        db, cursor = self.connect()
        cursor.execute('INSERT INTO `inv`(`owner_id`, `item_id`, `count`) VALUES ({},{},{})'.format(userid, itm, count))
        db.commit()      
        self.disconnect(db)


    def get_shop_list(self):
        db, cursor = self.connect()
        cursor.execute('SELECT * FROM `items`')
        res = cursor.fetchall()
        l = []
        for i in res:
            ia = item.item(i[0])
            l.append(str(ia))
        return l 
        self.disconnect(db)




    def set_prefix(self, guild, prefix):
        db, cursor = self.connect()
        cursor.execute('INSERT INTO `prefixes`(`serverid`, `prefix`) VALUES ({},"{}")'.format(guild, prefix))
        db.commit()
        self.disconnect(db)

    def get_prefix(self, guild):
        db, cursor = self.connect()
        self.del_prefix(guild)
        cursor.execute('SELECT * FROM `prefixes` WHERE serverid = {}'.format(guild))
        res = cursor.fetchall()
        if len(res) == 0:
            return ';'
        self.disconnect(db)
        return res[0][1]

    def del_prefix(self, guild: discord.Guild):
        db, cursor = self.connect()
        try:
            cursor.execute('DELETE FROM `prefixes` WHERE serverid = {}'.format(guild))
            db.commit()
            self.disconnect(db)
        except Exception as e:
            pass


    def get_prefixes(self):
        db, cursor = self.connect()
        cursor.execute('SELECT * FROM `prefixes`')
        res = cursor.fetchall()
        dict_ = {}
        for i in res:
            dict_[i[0]] = i[1]
        self.disconnect(db)
        return dict_
    def get_user_top_raw(self):
        db, cursor = self.connect()
        cursor.execute('SELECT * FROM user_leveling')
        rd = cursor.fetchall()
        r = {}
        ind = 0
        for i in len(rd) - 1:
            r[rd[ind]] = rd[2]
        self.disconnect(db)
        return r
    

    def create_user_profile(self, user: discord.User):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.execute("INSERT INTO user_leveling (user_id, level, xp, gold) VALUES ({}, {}, {}, {})".format(user.id, 1,0, 0))

            db.commit() 
            self.disconnect(db)
        else:
            self.disconnect(db)
            return

    def get_user_leveling(self, user: discord.User):
        db, cursor = self.connect()
        inf = {'user_id': user.id, 'level': 0, 'xp': 0, 'gold':0}
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        d = res[0]
        inf['level'] = d[1]
        inf['xp'] = d[2]
        inf['gold'] = d[3]
        self.disconnect(db)
        return inf




    def add_exp(self, user: discord.User, count: int):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if(len(res) == 0):
            self.disconnect(db)
            raise Exception("This user is not exits!")

        mapa = self.get_user_leveling(user)

        cursor.execute('UPDATE `user_leveling` SET `level`={},`xp`={} WHERE user_id={}'.format(mapa['level'], mapa['xp'] + count, mapa['user_id']))
        self.disconnect(db)
        db.commit()


    def remove_gold(self, user: discord.User, count: int):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if(len(res) == 0):
            self.disconnect(db)
            raise Exception("This user is not exits!")
        mapa = self.get_user_leveling(user)
        cursor.execute('UPDATE `user_leveling` SET`gold`={} WHERE user_id = {}'.format(mapa['gold'] - count, user.id))
        db.commit()
        self.disconnect(db)

        
    def add_gold(self, user: discord.User, count: int):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if(len(res) == 0):
            self.disconnect(db)
            raise Exception("This user is not exits!")

        mapa = self.get_user_leveling(user)

        cursor.execute('UPDATE `user_leveling` SET `gold`={} WHERE user_id={}'.format(mapa['gold'] + random.randrange(101), mapa['user_id']))

        db.commit()
        self.disconnect(db)




    def level_up(self, user: discord.User):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_leveling WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if(len(res) == 0):
            raise Exception("This user is not exits!")
            self.disconnect(db)


        mapa = self.get_user_leveling(user)

        cursor.execute('UPDATE `user_leveling` SET `level`={},`xp`={} WHERE user_id={}'.format(mapa['level'] + 1, 0, mapa['user_id']))
        db.commit()
        self.disconnect(db)
    """
    Social fish .-.
    """

    def create_user_socail_profile(self, user: discord.User):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.execute(f"INSERT INTO `user_info` (`user_id`, `description`) VALUES ({user.id},\"Not provided\")")

            db.commit() 
            self.disconnect(db)
        else:
            self.disconnect(db)
            return

    def edit_desc(self, user: discord.User, description: str):
        db, cursor = self.connect()
        cursor.execute("SELECT * FROM user_info WHERE user_id={}".format(user.id))
        res = cursor.fetchall()
        if(len(res) == 0):
            raise Exception("This user is not exits!")

        cursor.execute('UPDATE `user_info` SET `description`=\"{}\" WHERE user_id={}'.format(description, user.id))

        db.commit()
        self.disconnect(db)

    def get_user_desc(self, user: discord.User):
        db, cursor = self.connect()
        cursor.execute('SELECT description FROM user_info WHERE user_id={}'.format(user.id))

        res = cursor.fetchall()[0][0]
        self.disconnect(db)
        return res



    """
    Osu! module
    """

    def create_profile(self, user: discord.User, osu_name: str):
        db, cur = self.connect()
        cur.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        res = cur.fetchall()
        if(len(res) != 0):
            raise Exception('You already setuped Lol')
        r = requests.get(f'https://osu.ppy.sh/api/get_user?k={config.osu_token}&u={osu_name}')
        r = r.json()[0]
        osu_id = r['user_id']
        q = 'INSERT INTO `user_keys`(`user_id`, `server_user_id`) VALUES ({},"{}")'.format(user.id, osu_id)
        cur.execute(q)

        db.disconnect()
        db.commit()

    def user_profile_exits(self, user: discord.User):
        db, cur = self.connect()
        query = 'SELECT * FROM user_keys WHERE user_id={}'.format(user.id)
        cur.execute(query)
        db.disconnect()
        res = cur.fetchall()
        if(len(res) == 0):
            return False
        else:
            return True

    def get_profile(self, user: discord.User):
        db, cur = self.connect()
        cur.execute('SELECT * FROM user_keys WHERE user_id={}'.format(user.id))
        res = cur.fetchall()
        if(len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': user.id,'osu_id':res[0][1]}
            
            return inf

    def get_profile_id(self, userid):
        db, cur = self.connect()
        cur.execute('SELECT * FROM user_keys WHERE user_id={}'.format(userid))
        res = cur.fetchall()
        if(len(res) == 0):
            raise Exception('You Not registred setuped Lol')
        else:
            inf = {'user_id': userid,'osu_id':res[0][1]}
            
            return inf
            

    



        

        

    
