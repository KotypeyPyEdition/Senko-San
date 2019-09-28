import aioredis
import asyncio
import config
class Redis:
    def __init__(self, host='localhost'):
        self.host = host


    async def get(self, key) -> str:
        conn = await aioredis.create_connection(self.host)
        res = await conn.execute('get', key)

        conn.close()
        await conn.wait_closed()
        return res


    async def set(self, key, value):
        conn = await aioredis.create_connection(self.host)
        res = await conn.execute('set', key, value)
        conn.close()
        await conn.wait_closed()
        return res




