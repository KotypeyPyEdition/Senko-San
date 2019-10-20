import discord
from random import choice, randrange
import asyncio
from utils import database
from classes import item


class Pm:
    def __init__(self, ctx, atacker, defender, max_hp=100):
        self.ctx = ctx
        self.bot = self.ctx.bot
        self.aid = int(atacker)
        self.did = int(defender)
        self.colors = [discord.Colour.teal(), discord.Colour.blue(), discord.Colour.orange(), discord.Colour.green(), discord.Colour.red(), discord.Colour.magenta()]
        self.db = database.DBUtils(ctx.bot)
        self.hp = {}
        
        

    async def start(self):
        await self.ctx.send('[I] this command is only experemental, you can meet bugs')
        self.skip_streak = 0
        self.atacker = await self.bot.fetch_user(self.aid)
        self.defender = await self.bot.fetch_user(self.did)
        self.turn = self.atacker
        self.chached_inv = {}
        self.chached_inv[self.aid] =  {}
        self.chached_inv[self.did] = {}
        self.hp[self.aid] = 100
        self.hp[self.did] = 100
        self.hp['max'] = 100
        embed = discord.Embed(title="PvP call")
        embed.set_thumbnail(url=self.atacker.avatar_url_as(format="png", size=128))
        embed.add_field(name=':crossed_swords: Attacker', value=self.atacker.name, inline=True)
        embed.add_field(name=':shield: Defender', value=self.defender.name, inline=True)
        embed.set_footer(text=f'{self.defender.name} have 15 seconds to accept or deny call!')
        embed.add_field(name='INFO', value=f'{self.defender.mention} `Please type "yes" or "no" to play`')
        embed.colour = choice(self.colors)#### color
        self.message = await self.ctx.send(embed=embed)
        try:
            self.call_message = await self.bot.wait_for('message', check=lambda m: m.author.id == self.defender.id and m.channel.id == self.ctx.message.channel.id, timeout=15)
        except asyncio.TimeoutError as e:
            await self.message.edit(content=f"{self.defender.mention} you took to long", embed=None)
        else:
            if self.call_message.content == 'yes':
                await self.message.delete()
                await self.start_fight()
            else:  # сохранись
                await self.ctx.send('fight is canceled BAKA!')

    async def start_fight(self):
        self.turn = self.atacker
        await self.wait_for_turn(self.turn)

    async def wait_for_turn(self, turn):
        embed = discord.Embed(title=f'{self.turn.name}`s turn')
        embed.colour = choice(self.colors)### если не работает изменить на 'color'
        embed.set_thumbnail(
            url=self.turn.avatar_url_as(format='png', size=128))
        embed.add_field(name='Select', value='Press :crossed_swords: to attack \n press 🚪 to run!')
        embed.add_field(name='Conditions',value='Max :heart: : {}'.format(self.hp['max']))
        embed.add_field(name=':crossed_swords: attacker`s :heart:', value=self.hp[self.aid], inline=True)
        embed.add_field(name=':shield: defender`s :heart:', value=self.hp[self.did], inline=True)
        tmp_msg = await self.ctx.send(embed=embed)
        await tmp_msg.add_reaction('⚔')
        await tmp_msg.add_reaction('🚪')
        try:
            r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: r.message.id == tmp_msg.id and u.id == self.turn.id, timeout=30)
        except asyncio.TimeoutError as e:
            await self.ctx.send('Skipping turn... (Reason: Time out)')
            await self.next_turn()
        else:
            await tmp_msg.delete()
            if str(r) == '⚔':
                await self.select_weapon()
            elif str(r) == '🚪':
                await self.exit()




    async def next_turn(self):
        if self.hp[self.aid] <= 0 and self.hp[self.did]:
            pass
        if self.hp[self.aid] <= 0:
            return await self.win(self.did)
        elif self.hp[self.did] <= 0:
            return await self.win(self.aid)
        if self.turn == self.atacker:
            self.turn = self.defender
        else:
            self.turn = self.atacker
        await self.wait_for_turn(self.turn)

    async def select_weapon(self):
      await self.cng_weapon()

    async def cng_weapon(self):
        inv = self.chached_inv[self.turn.id]
        inv2 = []
        counter = 0
        self.tmp_items = {}
        for i in inv:
            counter += 1
            self.tmp_items[counter] = i
            inv2.append(f'{counter} | {i.title} **PWR** {i.power}')
            inv2.append('\n\n0 - give a slap')
        if len(inv) == 0:
            inv = 'Empty inventory'
            self.tmp_items = {}
        else:
            
            inv = '\n'.join(inv2)

        
        embed = discord.Embed(title='Select weapon!',color=choice(self.colors), description=inv)
        embed.set_footer(text='You have 30 seconds')
        s = await self.ctx.send(embed=embed)

        try:
            m = await self.bot.wait_for('message', check=lambda m: m.author.id == self.turn.id and m.channel.id == self.ctx.channel.id, timeout=15)
        except asyncio.TimeoutError as e:
            await self.ctx.send('Skipping turn... (Reason: Time out)')
            await self.next_turn()
        else:
            await s.delete()
            if m.content == '0':
                await m.delete()
                rand_damage = randrange(50)
                eid = await self.enemy_id()
                self.hp[eid] -= rand_damage
                enemy = await self.enemy()
                await self.ctx.send(f'{self.turn.name} attacked {enemy.name} for {rand_damage}HP', delete_after=5)
                await self.next_turn()
            elif int(m.content) > 0 and int(m.content) in self.chached_inv[self.turn.id]:
                item_id = int(m.content)
                await m.delete()
                self.s_item = item.item(self.tmp_items[item_id])
                eid = await self.enemy_id()
                self.hp[eid] -= self.s_item.power
                enemy = await self.enemy()
                await self.ctx.send(f'{self.turn.name} attacked {enemy.name} for {self.s_item.power}HP', delete_after=5)
                await self.next_turn()
            else:
                await self.ctx.send('Unknown item')
                await self.select_weapon()

    async def exit(self):
        enemy = await self.enemy_id()
        await self.win(enemy)


    async def win(self, uid):
        usr = await self.bot.fetch_user(uid)
        random_gold = randrange(100)
        random_raiting = randrange(30)
        win_embed = discord.Embed(title=f'{usr.name} win!', color=choice(self.colors), description=f'{usr.name} is a winner he now will get a rewards')
        win_embed.set_thumbnail(url=usr.avatar_url_as(format='png', size=128))
        emote = discord.utils.get(self.bot.emojis, name='Gold_Nugget')
        win_embed.add_field(name='Prizes', value=f'+{random_raiting} raiting\n +{random_gold} {str(emote)}')
        await self.ctx.send(embed=win_embed)
        await self.end_fight()


    async def end_fight(self):
        await self.ctx.send('Fight ended!')
    async def enemy(self):
        if self.turn == self.atacker:
            return self.defender
        else:
            return self.atacker

    async def enemy_id(self):
        if self.turn == self.atacker:
            return self.did
        else:
            return self.aid

    async def enemy_hp(self):
        if self.turn == self.atacker:
            return self.hp[self.did]
        else:
            return self.hp[self.aid]
