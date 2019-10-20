import discord
from discord.ext import commands
import asyncio
from PIL import Image, ImageDraw
from utils import paginator
from main import SenkoSanBot
from random import randrange
class Utils(commands.Cog):
    def __init__(self, bot: SenkoSanBot):
        self.bot = bot
        self.commands = {}

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(name='help')
    async def help_cmd(self, ctx: commands.Context, command=None):
        '''

        shows this message
        '''
        h = paginator.Paginator(ctx, self.bot, 'Commands')
        if not command:
            cogs = self.bot.cogs
            for cog in cogs:
                if cog not in ['Events', 'Jishaku', 'Exp', 'Leveling', 'Social', 'Utils', 'Event', 'Admin', 'DBL'] and cog.replace(' ', '') != '':
                    commands = ', '.join([x.name for x in self.bot.commands if x.cog_name == cog and not x.hidden]) or "None"
                    h.add_page(paginator.Entry(name=cog, value=commands))
            await h.paginate()
        else:
            async def check(commandss):
                cmd = self.bot.get_command(commandss)
                if not cmd:
                    return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), title='Not found', description='Can`t find this command'))
                return cmd
            res = await check(command)
            r = randrange(255)
            g = randrange(255)
            b = randrange(255)
            emned = discord.Embed(colour=discord.Colour.from_rgb(r,g,b), title=f'About {res} command', description=res.help)
            await ctx.send(embed=emned)


def setup(bot):
    bot.add_cog(Utils(bot))
                
