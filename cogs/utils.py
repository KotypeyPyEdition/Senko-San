import discord
from discord.ext import commands
import asyncio
from PIL import Image, ImageDraw
from utils import paginator
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}


    @commands.command(name='help')
    async def help_cmd(self, ctx, command=None):
        h = paginator.Paginator(ctx, self.bot, 'Commands')
        if not command:
            cogs = self.bot.cogs
            for cog in cogs:
                if cog not in ['Events', 'Jishaku', 'Exp', 'Leveling', 'Social', 'Utils', 'Event', 'Admin'] and cog.replace(' ', '') != '':
                    commands = ', '.join([x.name for x in self.bot.commands if x.cog_name == cog and not x.hidden]) or "None"
                    h.add_page(paginator.Entry(name=cog, value=commands))
            await h.paginate()
    def split(self, list):
        list2 = []
        for x in list:
            list2.append(f"{x} - {list[x]}\n")

        return ' '.join(list2)



def setup(bot):
    bot.add_cog(Utils(bot))
                