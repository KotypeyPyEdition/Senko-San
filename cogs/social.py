from discord.ext import commands
import discord
import utils.database as dbu
class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Social(bot))