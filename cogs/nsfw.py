from nekos import nekos
from discord.ext import commands
import discord

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def neko(self, ctx, *, tag=None):
        return await ctx.send("Disabled due Discord ToS")
        

def setup(bot):
    bot.add_cog(Nsfw(bot))
