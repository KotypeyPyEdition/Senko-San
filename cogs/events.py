 

from discord.ext import commands
import discord
import mysql.connector
import traceback
import requests
import config
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, m):
        if m.author.bot:
            return
        cnt = m.content.lower()
        if cnt in config.aliases:
            ctx = await self.bot.get_context(m)
            cmd = self.bot.get_command(config.aliases[cnt])
            await ctx.invoke(cmd)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.BotMissingPermissions):

            x = []
            counter = 0
            for i in error.missing_perms:
                counter += 1
                x.append(f'{counter} - {i}')
            msg = """
>>> Bot need the following permissions:
```markdown
{}
```
               """.format('\n'.join(x))
            await ctx.send(msg)
        elif isinstance(error, commands.MissingPermissions):


            x = []
            counter = 0
            for i in error.missing_perms:
                counter += 1
                x.append(f'{counter} - {i}')
            msg = """
>>> You need the following permissions:
```markdown
{}
```
               """.format('\n'.join(x))
            await ctx.send(msg)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'>>> Error: this command has a delay, wait {error} seconds before use')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.NotOwner):
            await ctx.send('тебе это низя! ненене {}'.format(config.emojis['smug']))
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Not enough arguments')
        elif isinstance(error, discord.Forbidden):
            await ctx.send('Kindly provide me the permissions to do so')
        elif isinstance(error, discord.ext.commands.CheckFailure):
            disabled = ', '.join(config.disabled_commands)
            await ctx.send(f'Oh, no looks this command is disabled for you (currently disabled commands: `{disabled}`) due rewriting from mysql to redis')
        else:
            
            embed = discord.Embed(title="Catched an error! {}".format(config.emojis['ears']))
            embed.color = 0xff0008
            cmd = ctx.command.qualified_name.split(' ')
            
            try:
                from hastebin import post
                tr = post('\n'.join(traceback.format_tb(error.__traceback__)))
                embed.add_field(name="Traceback link(hastebin)", value="[click here]({})".format(tr), inline=True)
            except:
                embed.add_field(name='Error', value='Hastebin server is down can`t post error', inline=True)

            embed.add_field(name='In guild / channel', value=f'{ctx.message.guild.name} / <#{ctx.message.channel.id}>', inline=True)
            embed.add_field(name='By name / id', value=f'{ctx.message.author.name} / {ctx.message.author.id}', inline=True)
            embed.add_field(name='Command', value=cmd)
            embed.add_field(name='error message', value=error)
            admin = await self.bot.fetch_user(394879199325847562)
            await admin.send(embed=embed)
            await ctx.send(embed=embed)
            await ctx.send('Don\'t worry, I will send this message to my owner. Just wait, he will fix it!')





def setup(bot):
    bot.add_cog(Event(bot))
