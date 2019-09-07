import discord
import collections
import asyncio
__all__ = ('EmojiSettings')
from random import choice
EmojiSettings = collections.namedtuple('EmojiSettings', 'start back forward end close')
EMOJI_DEFAULT = EmojiSettings(
    start="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
    back="\N{BLACK LEFT-POINTING TRIANGLE}",
    forward="\N{BLACK RIGHT-POINTING TRIANGLE}",
    end="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
    close="\N{BLACK SQUARE FOR STOP}"
)

class Entry:
    def __init__(self, name, value, image=None):
        self.name = name
        self.value = value
        self.image = image


class Paginator:
    def __init__(self, ctx, bot, title):
        self.ctx = ctx
        self.bot = bot
        self.emojis = EMOJI_DEFAULT
        self.title = title
        self.pages = []
        self.active  = True
        self.colors = [discord.Colour.teal(), discord.Colour.blue(), discord.Colour.orange(), discord.Colour.green(), discord.Colour.red(), discord.Colour.magenta()]


    def filter(self, reaction: discord.Reaction, user: discord.User):
        return user.id == self.ctx.message.author.id


    async def paginate(self):
        self.message = await self.ctx.send('Wait...')
        message = self.message
        self.page_c = 0
        page_c = self.page_c
        page = self.pages[page_c]
        for reaction in self.emojis:
            await message.add_reaction(reaction)

        embed = discord.Embed(title=page.name, description=page.value)
        if page.image == None:
            pass
        else:
            embed.set_image(url=page.image)

            
        embed.set_footer(text='page {}/{}'.format(page_c + 1, len(self.pages)))
        embed.set_thumbnail(url=self.ctx.author.avatar_url_as(format='png', size=128))
        embed.color = choice(self.colors)
        await message.edit(embed=embed, content='None')
        
        while self.active == True:
            try:
                r, u = await self.bot.wait_for('reaction_add', check=lambda r,u: u.id == self.ctx.author.id and r.message.id == message.id, timeout=120)
            except asyncio.TimeoutError as e:
                try:
                    await self.message.edit(embed=None, content='Timed out')
                    self.active = False
                except Exception as e:
                    await self.ctx.send("WHO DELETED MESSAGE? BAKA!")
                    self.active = False


                
            else:
                if str(r) == '▶':
                    p = self.page_c + 1 

                    await self.to_page(p)
                elif str(r) == '◀':
                    p = self.page_c - 1
                    

                    await self.to_page(p)

                elif str(r) == '⏭':
                    p = self.page_c + 2

                    await self.to_page(p)
                elif str(r) == '⏮':
                    p = self.page_c - 2

                    await self.to_page(p)
                elif str(r) == '⏹':
                    self.active = False
                    await self.message.delete()
                    


    def add_page(self, page: Entry):
        self.pages.append(page)


    async def to_page(self, page):
        
        if page == len(self.pages):
            return
        elif page < 0:
            return

        self.page_c = page
        page = self.pages[self.page_c]
        embed = discord.Embed(title=page.name, description=page.value)

        if page.image == None:
            pass
        else:
            embed.set_image(url=page.image)
        
            
        
        embed.set_footer(text='page {}/{}'.format(self.page_c + 1, len(self.pages)))
        embed.set_thumbnail(url=self.ctx.author.avatar_url_as(format='png', size=128))
        embed.color = choice(self.colors)
        await self.message.edit(embed=embed, content=None)

