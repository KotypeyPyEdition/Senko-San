from discord.ext import commands
import utils.database as ud
import discord
from utils import pm
from utils import ticktock
class Rpg(commands.Cog, name='Games'):
    def __init__(self, bot):
        self.bot = bot
        self.d = ud.DBUtils(self.bot)

    @commands.is_owner()
    @commands.command()
    async def ttt(self, ctx: commands.Context, target: discord.Member=None):
        if not target:
            return await ctx.send('Usage: sen!ttt @user#1234')
        ttt = ticktock.TickTock(ctx, target)
        await ttt.prestart()

    @commands.command(name='pvp')
    async def pvp(self, ctx, target: discord.Member=None, bid=0):
        if not target:
            await ctx.send(f'usage {ctx.prefix}pvp @user#1234')
            return
        manager = pm.Pm(ctx, ctx.author.id, target.id)
        await manager.start()                                                           
def setup(bot):
    bot.add_cog(Rpg(bot))
