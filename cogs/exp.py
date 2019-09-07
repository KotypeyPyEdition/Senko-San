from discord.ext import commands
import discord
import utils.imaging as im
import utils.database as dbu
import os
from utils import paginator
class Exp(commands.Cog):
    """
    Experemental commands
    """

    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command(name='exp')
    async def exp(self, ctx, command=None):
        pass
def setup(bot):
    bot.add_cog(Exp(bot))