import discord
import asyncio
import io
import json
import traceback
from discord.ext import commands
import textwrap
from utils import database
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.team = [394879199325847562]

        
    @commands.command(name='unload', description='Unload a module(cog)', brief='load a module(cog)')
    async def unloaded(self, ctx, *, extension):   
        if ctx.author.id in self.team:
            extension = f'cogs.{extension}'
            try:
                self.bot.unload_extension(extension)
            except Exception as e: 
                await ctx.send(f'Не удалось отключить модуль {extension}.\n{e}')
            else:
                embed=discord.Embed(title="Unloaded", description=f"Module {extension} has been unloaded.")
                await ctx.send(embed=embed)
        else:
            await ctx.send('Вы не мой админ!')
    
    @commands.command(name='load', description='load a module(cog)', brief='load a module(cog)')
    async def loaded(self, ctx, *, extension):
        if ctx.author.id in self.team:
            extension = f'cogs.{extension}'
            try:
                self.bot.load_extension(extension)
            except Exception as e: 
                await ctx.send(f'Не удалось загрузить модуль {extension}.\n{e}')
            else:
                embed=discord.Embed(title="Loaded", description=f"Module {extension} has been loaded.")
                await ctx.send(embed=embed)
        else:
            await ctx.send('Вы не мой админ!')
    @commands.command(name='reload', description='reload a module(cog)', brief='reload a module(cog)')
    async def reload(self, ctx, *, extension): 
        if ctx.author.id in self.team:
            extension = f'cogs.{extension}'
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e: 
                await ctx.send(f'Не удалось перезагрузить модуль {extension}.\n{e}')
            else:
                embed=discord.Embed(title="Unloaded", description=f"Module {extension} has been reloaded")
                await ctx.send(embed=embed)
        else:
            await ctx.send('Вы не мой админ!')



            
    @commands.command(name="rl", description='stop the bot', brief='stop the bot')
    async def stop(self, ctx):
        if(ctx.author.id not in self.team):
            await ctx.send("GO AWAY FROM MY HOUSE")
        else:
            await ctx.send(":ok:")
            import os
            os.system("cd ..")
            os.system("start.cmd")
def setup(bot):
    bot.db = database.DBUtils()
    bot.add_cog(Admin(bot))
