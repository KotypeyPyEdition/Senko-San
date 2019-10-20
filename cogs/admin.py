import discord
import asyncio
import io
import json
import traceback
from discord.ext import commands
import textwrap
from utils import database
from utils import async_mysql
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.team = [394879199325847562]
        self.db = database.DBUtils(self.bot)

    @commands.is_owner()
    @commands.command()
    async def addgold(self, ctx: commands.Context, usr: discord.Member=None, count=None):
        if not usr or not count:
            return await ctx.send('Usage: ;addgold @user1234 1234')
        try:
            self.db.add_gold(usr.id, int(count))
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            await ctx.author.send(e)


    @commands.is_owner()
    @commands.command()
    async def rmgold(self, ctx: commands.Context, usr: discord.Member=None, count=None):
        if not usr or not count:
            return await ctx.send('Usage: ;addgold @user1234 1234')
        try:
            self.db.add_gold(usr.id, -int(count))
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            await ctx.author.send(e)

    @commands.is_owner()
    @commands.command(name="rl", description='stop the bot', brief='stop the bot')
    async def stop(self, ctx):
        if(ctx.author.id not in self.team):
            await ctx.send("GO AWAY FROM MY HOUSE")
        else:
            await ctx.send(":ok:")
            exit()
    @commands.is_owner()
    @commands.command()
    async def additem(self, ctx: commands.Context, usr: discord.Member=None, itm=None):
        if not usr or not itm:
            return await ctx.send('Usage: ;additem @user1234 1')
        self.db.add_item(usr.id, itm, 1)
        await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command()
    async def addxp(self, ctx: commands.Context, usr: discord.Member=None, itm=None):
        if not usr or not itm:
            return await ctx.send('Usage: ;addxp @user1234 1')
        self.db.add_xp(usr.id, itm)
        await ctx.message.add_reaction("✅")

    @commands.is_owner()
    @commands.command()
    async def eval(self, ctx, *, code):
        try:
            res = eval(code)
        except Exception as e:
            await ctx.send(e)
        
        await ctx.send(res)

def setup(bot):
    bot.add_cog(Admin(bot))
