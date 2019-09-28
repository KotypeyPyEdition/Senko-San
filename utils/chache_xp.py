from utils import async_mysql
import config

class chache:

    """
    Data chaching for bot

    Its saves in to dict and when timeout finished it will sent data to mysql server
    """
    def __init__(self):
        self.host = config.mysql_host
        self.user = config.mysql_user
        self.password = config.mysql_password
        self.database = config.mysql_database
        self.chached_users = {}
        self.sql = async_mysql.Sql()


    def update_chached_data(self, userid, data: dict):
        """
        update local user data

        usage: update_chached_data(123456, {level: 1, xp: 0, gold: 1})
        """
        if userid not in self.chached_users:
            self.chached_users[userid] = {'xp': 0, 'level': 0, 'gold': 0}
        self.chached_users[userid]['xp'] = data['xp']
        self.chached_users[userid]['level'] = data['level']
        self.chached_users[userid]['gold'] = data['gold']


    async def send_data(self):
        for i in self.chached_users:
            temp_data = await self.sql.execute('SELECT * FROM user_leveling WHERE user_id={}'.format(i))
            if len(temp_data) == 0:
                query = 'INSERT INTO `user_leveling`(`user_id`, `level`, `xp`, `gold`) VALUES ({},{},{},{})'.format(i, i['level'], i['xp'], ['gold'])
                await self.sql.execute(query)
                return

            level = str(self.chached_users[i]['level'])
            xp = str(self.chached_users[i]['level'])
            gold = str(self.chached_users[i]['level'])
            uid = str(i)
            query = "UPDATE `user_leveling` SET `level`={},`xp`={} gold={} WHERE user_id={}".format(level,xp,gold,uid)
            await self.sql.execute(query)

