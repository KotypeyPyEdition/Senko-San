import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import os
from utils import paginator
import utils.database as dbu
import classes.item
import asyncio
import textwrap
import random
import qrcode
import io
import json
import apiai
import config
import requests
import time
import datetime
from functools import partial
from utils import imaging
class User(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.d = dbu.DBUtils(self.bot)
		self.img_utils = imaging.ImgUtils(self.bot)
	@commands.cooldown(1.0, 8, commands.BucketType.user)
	@commands.command(name="me")
	async def me(self, ctx):
		func = partial(self.img_utils.profile_image, ctx.author)
		a = await self.bot.loop.run_in_executor(None, func)
		await ctx.send('disabled')



	@commands.command()
	async def top(self, ctx):
		db, cursor = dbu.DBUtils().connect()
		cursor.execute('SELECT * FROM user_leveling')
		db2 = cursor.fetchall()
		db3 = {}
		for i in db2:
			db3[i[0]] = i[3]
		raw = db3
        
		board = sorted(raw.items(), key=lambda x: x[1], reverse=True)[:10]
		counter = 0
		leaderboard = []
		for x in board:
			user = self.bot.get_user(int(x[0]))
			if not user:
				continue
			coins = x[1]
			counter += 1
			leveling = dbu.DBUtils().get_user_leveling(user)



            #Emojis
			Xp_bottle = discord.utils.get(self.bot.emojis, name='Xp_bottle')
			Xp = discord.utils.get(self.bot.emojis, name='Xp')
			gold = discord.utils.get(self.bot.emojis, name='Gold_Nugget')
			
			
			user_xp = f"{str(leveling['xp'])}/ {str(leveling['level'] * 300)}"
			user_lvl = str(leveling['level'])
			
			leaderboard.append(f'`{counter}` | **{user}** :: `{coins}` {str(gold)}, {str(Xp_bottle)} `{user_lvl}`, {str(Xp)} `{user_xp}`')
		e = discord.Embed()
		e.description = '\n'.join(leaderboard)
		e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
		e.set_footer(text=ctx.prefix + ctx.command.qualified_name, icon_url=ctx.guild.me.avatar_url)
		e.color = ctx.guild.me.color
		db.disconnect()
		await ctx.send(embed=e)
		


	@commands.command()
	async def profile_edit(self, ctx):
		func_list = ['description']
		args = ctx.message.content.split(' ')
		if(len(args) == 1):
			await ctx.send(f':x: you need to provide functions! function list: `{" ".join(func_list)}`')
			return
		func = args[1]
		if(func not in func_list):
			await ctx.send(f':x: function {func} not found, function list: `{" ".join(func_list)}``')
			return
		elif func == 'description':
			if len(args) == 2:
				await ctx.send(':x: you must to provide desciprion')
				return
			db = dbu.DBUtils()
			c = ctx.message.content.split(' ')
			del c[0]
			del c[0]
			c = ' '.join(c)
			db.edit_desc(ctx.message.author, c)
			await ctx.send(f"i setted your profile description to `{c}`")
			
	@commands.command()
	@commands.bot_has_permissions(manage_webhooks=True)
	async def mebot(self, ctx, *, msg: commands.clean_content):
		await ctx.message.delete()
		w = await ctx.channel.create_webhook(name=ctx.author.name)
		await w.send(msg, avatar_url=ctx.author.avatar_url)
		
		await w.delete()

	@commands.command(name='web', aliases=['support'])
	async def web(self, ctx):
		await ctx.send('**Support me or view statistic on http://src-bot.tk/**')


	@commands.command(name='invite')
	async def invite(self, ctx):
		embed = discord.Embed(title="UwU you want invite me?", colour=discord.Colour(0x45487a), description="to invite me [click here](https://discordapp.com/api/oauth2/authorize?client_id=598492095682052097&permissions=8&scope=bot)")
		await ctx.send(embed=embed)



	@commands.command(name='shop')
	async def shop(self, ctx):
		db = dbu.DBUtils()
		res = db.get_shop_list()
		embed = discord.Embed(title='shop', description='\n'.join(res))
		embed.color = 0x1abcc4
		await ctx.message.channel.send(embed=embed)
	@commands.command()
	async def buy(self, ctx, item=None):
		if item == None:
			await ctx.send('Provide item!')
			return
		try:
			item = classes.item.item(item)
		except Exception as e:
			await ctx.send('Item not found!')
		else:
			mapa = self.d.get_user_leveling(ctx.author)
			if(item.cost > mapa['gold']):
				await ctx.send('Not enougt gold!')
				return
			
			embed = discord.Embed(title='confrimation', description='Press ✅ to buy it for cancel press ❎')
			embed.add_field(name='Item', value=str(item))
			message = await ctx.send(embed=embed)


			try:
				await message.add_reaction('✅')
				await message.add_reaction('❎')
				r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: r.message.id == message.id and u.id == ctx.author.id, timeout=15)
			except asyncio.TimeoutError as e:
				await message.edit(content='Timed out')
			else:
				if str(r) == '❎':
					await ctx.send('canceled')
				elif str(r) == '✅':
					self.d.remove_gold(ctx.author, item.cost)
					self.d.add_item(ctx.author.id, item.id)
					await ctx.send('✅ you now have 1 {}'.format(item.title))




	@commands.command()
	async def minesweeper(self, ctx, size='10x10'):
		size = size.split('x')
		text = ''
		if int(size[0]) > 14 or int(size[1]) > 14 or int(size[0]) < 1 or int(size[1]) < 1:
			await ctx.send('size must be not lower than 1x1 and not bigger that 14x14')
			return
		else:
			bombs = 0
			for i in range( int(size[0]) ):
				for i in range( int(size[1]) ):
					element = random.choice([':two:', ':one:', ':zero:', ':bomb:']) 
					text += '||' + element+ '||'
					if element == ':bomb:':
						bombs += 1
				text += '\n'
			await ctx.send(f'Teritory {size[0]}x{size[1]} with {bombs} bombs\n{text}')


	@commands.command(name='ai')
	async def ai(self, ctx, *, message=None):
		if not message:
			await ctx.send(f'Usage: {ctx.prefix}ai hello')
			return
		request = apiai.ApiAI(config.apiai).text_request()  # Токен API к Dialogflow
		request.lang = 'en'  # На каком языке будет послан запрос
		#request.session_id = 'Batlab'  # ID Сессии диалога (нужно, чтобы потом учить бота)
		request.query = message  # Посылаем запрос к ИИ с сообщением от юзера
		responseJson = json.loads(request.getresponse().read().decode('utf-8'))
		response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
		if response:
			await ctx.send(response)
		else:
			await ctx.send('I don`t understand you')

	@commands.command()
	async def home(self, ctx):
		await ctx.send('Home here -> **https://discord.gg/vs7qj5q**')


	@commands.command()
	async def py(self, ctx, *, kod=None):
		if not kod:
			await ctx.send('Usage: ;py {code}')
			return
		message = await ctx.send(embed = discord.Embed(title='Python executor', color=discord.Colour.green(), description=f'```Waiting for response```'))
		cur_time = int(time.time())
		kod = kod.replace('```', ' ')
		kod = kod.replace('py', ' ')
		kod = kod.replace('```', ' ')
		po = {"cmd": 'python main.cpp', "src": kod}
		r = requests.post('http://coliru.stacked-crooked.com/compile', data=json.dumps(po))
		tim = int(time.time())
		res = r.text
		if len(res) == 0:
			res = 'No output'
		else:
			res = r.text[:1000]
		embed = discord.Embed(title='Python executor', color=discord.Colour.green(), description=f'```{res}```')
		embed.set_footer(text='Executed in {} seconds'.format(tim - cur_time))

		await message.edit(embed=embed)


	@commands.command()
	async def blacklist(self, ctx):
		r = self.bot.blacklisted_cache
		pag = paginator.Paginator(ctx, self.bot, 'None')
		for i in r:
			try:
				usr = await self.bot.fetch_user(i['id'])
				fullname = f'{usr.name}#{usr.discriminator}'
			except Exception as e:
				fullname = 'Cannot get data maybe i don`t have mutual server with this user'
			
			pag.add_page(paginator.Entry(fullname, i['reason'], i['proof']))

		await pag.paginate()


	@commands.has_permissions(manage_message=True)
	@commands.command()
	async def set_name(self, ctx, *, name=None):
		if not name:
			return await ctx.send(f'Usage: {ctx.prefix}set_name name')
		name = name.replace(' ', '\u2009')
		await ctx.channel.edit(name=name)
		await ctx.send('Channel updated!')
	@commands.command()
	async def embed(self, ctx: commands.Context, *, code: str=None):

		help_ = """
		tags:
		footer : 'footer here'
		fields: [{'title': 'AAAAAA', 'value': 'ya oru kak bezbashiniy', 'inline': 0}] 
		title: 'title here'
		image: 'image_url'
		color: {'r': 0, 'g': 255, 'b': 0}
		author: {'name': 'uname', 'url': '<https://i.imgur.com/FyA5dhF.png>', icon_url='<https://i.imgur.com/FyA5dhF.png>'}
		timestamp: 0 - no, 1 or higher - yes
		thumbail: '<https://i.imgur.com/FyA5dhF.png>'
		description: 'description'
		example: ;embed `{'title': 'Hello', 'desciprion': 'AAAAAAAAAAAAAAAAA', 'footer': 'footer_here', 'fields': [{'title': 'mraz', 'value': '55x55'}, {'title': 'mi rezem kinolentu', 'value': '55x55'}], 'color': {'r':0, 'g':0,'b': 255}, 'image': '<https://i.imgur.com/SDd0M5y.png>'}`
		"""
		emj = discord.utils.get(self.bot.emojis, name='loading')
		await ctx.message.add_reaction(emj)

		if not code:
			return await ctx.send(help_)
		
		try:
			code = code.replace("'", "\"")
			codes = json.loads(code)
			embed = discord.Embed()
		except Exception as e:
			await ctx.send(f'Parse error: \n {e}')
		else:
			try:
				for i in codes:
					if i == 'title':
						embed.title = codes[i]
					elif i == "color":
						embed.colour = discord.Color.from_rgb(codes[i]['r'], codes[i]['g'], codes[i]['b'])
					elif i == "fields":
						for x in codes[i]:
							try:
								inline = x['inline']
							except Exception as e:
								x['inline'] = 0
							if x['inline'] == 0:
								inline=False
							else:
								inline=True
							embed.add_field(name=x['title'], value=x['value'], inline=inline)
					elif i == 'image':
						embed.set_image(url=codes[i])
					elif i == 'footer':
						embed.set_footer(text=codes[i])
					elif i == 'description':
						embed.description = codes[i]
					elif i == 'timestamp':
						if codes[i] == 0:
							embed.timestamp = None
						else:
							embed.timestamp = datetime.datetime.now()
					elif i == 'thumbail':
						embed.set_thumbnail(url=codes[i])
					elif i == 'author':
						embed.set_author(codes[i]['name'], url=codes[i]['url'], icon_url=codes[i]['icon_url'])
					
			except Exception as e:
				return await ctx.send(f'In Embed Build Excpetion: {e}')
			

			await ctx.send(embed=embed)


	@commands.command()
	async def report(self, ctx, userid=None, reason=None, proof=None):
		pass
def setup(bot):        
	bot.add_cog(User(bot))
