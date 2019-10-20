from discord.ext import commands
import discord
from random import randrange
import asyncio


class TickTock:
    def __init__(self, ctx: commands.Context, enemy: discord.Member):
        self.ctx = ctx
        self.bot = ctx.bot
        self.starter = ctx.author
        self.enemy = enemy
        self.turn = self.starter
        self.playground = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.x  =self.starter
        self.o = self.enemy
        #self.x = '❌'
        #self.o = '⭕'

    async def prestart(self):
        r = randrange(255)
        g = randrange(255)
        b = randrange(255)
        self.embed = discord.Embed(title='tic tac toe', colour=discord.Colour.from_rgb(r,g,b))
        self.embed.add_field(name=self.x, value=self.starter.name)
        self.embed.add_field(name=self.o, value=self.enemy.display_name)
        self.embed.add_field(name='INFO', value=f'{self.enemy.mention} type `yes` to start game')
        self.message = await self.ctx.send(embed=self.embed)
        try:
            m = await self.bot.wait_for('message', check=lambda m: m.author.id == self.enemy.id and m.channel.id == self.ctx.channel.id, timeout=15)
        except asyncio.TimeoutError as e:
            await self.message.delete()
            await self.ctx.send('tic tac toe canceled', delete_after=5.0)
        else:
            if m.content.lower() == 'yes':
                await m.delete()
                await self.start()
            else:
                await self.message.delete()
                await self.ctx.send('tic tac toe canceled', delete_after=5.0)


    async def start(self):

        r = randrange(255)
        g = randrange(255)
        b = randrange(255)
        self.embed = discord.Embed(title=f'{self.starter.name} VS {self.enemy.name} [Tick Tack Toe]', colour=discord.Colour.from_rgb(r,g,b))
        ls = []
        nl = [3,6,9]
        self.embed.description = ''.join(ls)
        await self.message.edit(content=None, embed=self.embed)
        await self.wait_for_turn(self.turn)

    async def wait_for_turn(self, turn):

        playg = await self.get_playground()
        await self.ctx.author.send(str(self.playground))
        self.embed.description = f'{self.turn.name}`s turn\n\n{playg}'
        await self.message.edit(content=None, embed=self.embed)
        try:
            m = await self.bot.wait_for('message', check=lambda m: m.author.id == turn.id and m.channel.id == self.ctx.channel.id, timeout=30)
        except asyncio.TimeoutError as e:
            await self.ctx.send('Skipping turn...')
            await self.next_turn()
        else:

            try:
                t = int(m.content)
            except:
                await self.ctx.send('Unknow turn try again', delete_after=5)
                await self.wait_for_turn(self.turn)
            team = await self.get_team(self.turn)
            await self.set_slot()
            await self.next_turn()


    async def get_team(self, turn):
        if turn.id == self.enemy:
            return '⭕'
        else:
            return '❌'

    async def get_playground(self):
        ls = []
        nl = [3,6,9]
        for i in range(len(self.playground)):
            for x in range(len(self.playground[i])):
                if self.playground[i][x] == None:
                    if not self.playground[i][x]:
                            ls.append('⬛')
                    elif x == self.o:
                            ls.append('⭕')
                    elif x == self.x:
                            ls.append('❌')
        return ''.join(ls)

    async def set_slot(self, floor:int, slot: int, turn: discord.Member):
        if self.playground[floor - 1][slot -1]:

            await self.ctx.send('This slot is already picked!', delete_after=5)

            await self.wait_for_turn(self.turn)


        team = await self.get_team(turn)

        self.playground[floor][slot] = team

    async def enemy_(self):
        if self.turn == self.starter:
            return self.enemy
        else:
            return self.starter

    async def next_turn(self):

        en = await self.enemy_()
        self.turn = en
        await self.wait_for_turn(self.turn)

