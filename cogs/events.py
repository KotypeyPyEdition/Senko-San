 

from discord.ext import commands
import discord
import mysql.connector
import traceback
import requests

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, m):
        if m.author.bot:
            return
        if('Sagiri' in m.content or 'Сагири' in m.content or 'eromanga' in m.content):
            await m.channel.send(f'I don\'t know anyone with this name( {self.bot.latency *1000} ms)')
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandInvokeError):
         await ctx.send(str(err))
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("You can use this command in NSFW channel")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("I dont have permissions to do this!")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"Error cooldown are enabled, wait {error} to use it again!", colour=discord.Colour(0xda1013))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            await ctx.send('тебе это низя! ненене')
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.send(error)
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Not enough arguments')
        elif isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.send('Looks you are in blacklist or bot`s check failed!')
        else:
            
            embed = discord.Embed(title="Catched an error!")
            embed.color = 0xff0008
            cmd = ctx.command.qualified_name.split(' ')
            
            try:
                from hastebin import post
                tr = post('\n'.join(traceback.format_tb(error.__traceback__)))
                embed.add_field(name="Traceback link(hastebin)", value="[click here]({})".format(tr), inline=True)
                file_ = None

            except BaseException:
                file_ = open("traceback.txt", "w")
                file_.write('\n'.join(traceback.format_tb(error.__traceback__)))
                file_.close()
                file_ = discord.File(fp="traceback.txt")

            embed.add_field(name='In guild / channel', value=f'{ctx.message.guild.name} / <#{ctx.message.channel.id}>', inline=True)
            embed.add_field(name='By name / id', value=f'{ctx.message.author.name} / {ctx.message.author.id}', inline=True)
            embed.add_field(name='Command', value=cmd)
            embed.add_field(name='error message', value=error)
            admin = await self.bot.fetch_user(394879199325847562)
            await admin.send(embed=embed)
            await admin.send(file=file_)
            await ctx.send(embed=embed)
            await ctx.send('Don\'t worry, I will send this message to my owner. Just wait, he will fix it!')





def setup(bot):
    bot.add_cog(Event(bot))
