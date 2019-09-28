import dbl
from discord.ext import commands, tasks
import config
class DBL(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.dbl = dbl.DBLClient(self.bot, config.dbl_key, webhook_path='/webhook', webhook_auth=config.token, webhook_port=8888)
    tasks.loop(minutes=10.0)
    async def send_data(self):
        try:
            await self.bot.dbl.post_guild_count()
            print('Posted guild count ({})'.format(len(self.bot.guilds)))
        except Exception as e:
            print('Cannot post guild count \n {}'.format(e))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        await self.bot.fetch_user(394879199325847562).send(data)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        await self.bot.fetch_user(394879199325847562).send(data)

        
def setup(bot: commands.Bot):
    bot.add_cog(DBL(bot))