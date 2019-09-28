import asyncio
import aiohttp
from discord.ext.commands import Bot
class API:
    def __init__(self, bot: Bot, token):
        self.bot = bot
        self.token = token
        self.stats_url = "https://discordbots.org/api/bots/" + str(bot.user.id) + "/stats"
        self.check_url = f"https://discordbots.org/api/bots/{str(bot.user.id)}/check"
        self.votes_url = f'https://discordbots.org/api/bots/{str(bot.user.id)}/votes'
        self.session = aiohttp.ClientSession()
        self.header = {"Authorization" : self.token}
    async def post_guilds(self):
        data = {'server_count': len(self.bot.guilds)}
        async with aiohttp.ClientSession() as client:
            await client.post(self.stats_url, data =data, headers=self.header)
        print('Server count posted')

    async def user_voted(self, userid: int):
        data = {'userid': userid}
        async with aiohttp.ClientSession().get(self.check_url + f'?userId={userid}', headers=self.header) as res:
            r = await res.json()
            res.close()
        if r['voted'] == 0:
            return False
        else:
            return True

    async def get_last_1000_votes(self) -> list:
        async with aiohttp.ClientSession().get(self.votes_url, headers=self.header) as res:
            r = await res.json()

        return r






