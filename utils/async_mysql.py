import aiomysql
import asyncio
import config
class Sql:
        def __init__(self):
            self.host = config.mysql_host
            self.user = config.mysql_user
            self.password = config.mysql_password
            self.database = config.mysql_database

        async def execute(self, query):
            conn = await aiomysql.connect(host=self.host, port=3306,
                                       user=self.user, password=self.password, db=self.database,)

            cur = await conn.cursor()
            try:
                await cur.execute(query)
            except Exception as e:
                res = str(e)
                await cur.close()
                conn.close()
            else:
                r = await cur.fetchall()
                if r:
                    res = r
                else:
                    res = cur.description
                await cur.close()
                conn.close()

            return res
