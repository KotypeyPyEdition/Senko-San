from discord.ext import commands
import utils.database as ud
import discord
from utils import pm

class Rpg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.d = ud.DBUtils()
        
        
    @commands.command(name='inventory', aliases=['inv'])
    async def inv(self, ctx):
        inv = self.d.get_user_inventory_list(ctx.author.id)
        l = []
        for i in inv:
            l.append("{} : PWR {}".format(i.title, i.power))
            
        if len(l) == 0:
            inv1 = 'there are only cockroaches'
        else:
            inv1 = '\n'.join(l)
        embed = discord.Embed(title='{}`s inventory'.format(ctx.author.name), description=inv1)
        embed.color = 0x26abbf
        
        await ctx.send(embed=embed)


    @commands.command(name='pvp')
    async def pvp(self, ctx, target=None, bid=0):
        if not target:
            await ctx.send(f'usage {ctx.prefix}pvp @user#1234')
            return
        target_ = target 
        manager = pm.Pm(ctx, ctx.author.id, target_)
        await manager.start()                                                           
def setup(bot):
    bot.add_cog(Rpg(bot))