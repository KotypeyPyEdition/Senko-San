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
    async def set(self, ctx: commands.Context, key=None, value=None):
        if not key and value or not key or not value:
            return await ctx.send('usage: ;set KEY VALUE')

        res = self.bot.redis.set(key, value)
        await ctx.send(res)

    @commands.is_owner()
    @commands.command()
    async def get(self, ctx: commands.Context, key=None):
        if not key:
            return await ctx.send('Usage: ;get KEY')

        try:
            res = self.bot.redis.get(key)
            await ctx.send(res)
        except Exception as e:
            res = str(e)
            await ctx.send('Not found')

    @commands.is_owner()
    @commands.command()
    async def add_item(self, ctx, user: discord.Member=None, item=None):
        if not user and item or not user or not item:
            return await ctx.send('Usage: ;add_item @user#0000 1')

        self.db.add_item(user.id, item)
        await ctx.send('added')
    @commands.is_owner()
    @commands.command()
    async def exec(self, ctx, *, cmd):
        try:
            self.bot.redis.execute_command(cmd)
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

def setup(bot):
    bot.add_cog(Admin(bot))
