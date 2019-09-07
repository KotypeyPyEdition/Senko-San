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
        else:
            async def check(command):
                aliases_cmds = [[y for y in x.aliases] for x in self.bot.commands]
                for aliases in aliases_cmds:
                    if command in aliases:
                        return True
                return False
            if command in [x.name for x in self.bot.commands] or await check(command) == True:
                command = [x for x in self.bot.commands if x.name == command or check(x.name) == True or command in x.aliases][0]
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, title=f'{ctx.prefix}{command.name} {command.signature}', description=command.help or "None", color=discord.Color.blue()).set_footer(text=f'{ctx.prefix}{ctx.command.name} {ctx.command.signature}'))
            else:  
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, title='Error', description='Unknown command', color=discord.Colour.red()).set_footer(text=f'{ctx.prefix}{ctx.command.name} {ctx.command.signature}'))
    def split(self, list):
        list2 = []
        for x in list:
            list2.append(f"{x} - {list[x]}\n")

        return ' '.join(list2)



def setup(bot):
    bot.add_cog(Utils(bot))
                