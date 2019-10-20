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
import random
import io
import json
import aiohttp
import apiai
import config
import requests
from googletrans import Translator
import time
import datetime
from functools import partial
from utils import imaging
from main import SenkoSanBot
class User(commands.Cog):
	def __init__(self, bot: SenkoSanBot):
		self.bot = bot
		self.d = dbu.DBUtils(self.bot)
		self.img_utils = imaging.ImgUtils(self.bot)
	@commands.cooldown(1.0, 8, commands.BucketType.user)
	@commands.command(name="me")
	async def me(self, ctx: commands.Context, usr:discord.Member = None):
		"""
		Usage: sen!me {member}

		Show your or Members profile
		"""
		if not usr:
			usr = ctx.author
		try:
			res = self.d.get_user_leveling(usr.id)
		except:
			await ctx.send('This user is not have leveling profile')
		else:
			
			gold = discord.utils.get(self.bot.emojis, name='senkocoins')
			xp = discord.utils.get(self.bot.emojis, name='Xp')
			xp_bottle = discord.utils.get(self.bot.emojis, name='Xp_bottle')
			embed = discord.Embed()
			embed.colour = discord.Color.green()
			embed.description = f"""
			{xp} : {res['xp']} / {res['level'] * 10}
			{xp_bottle} : {res['level']}
			{gold} : {res['gold']}


			You need {(res['level'] * 10) - res['xp']} xp to next level!
			"""
			embed.title = f'{usr.name}`s profile'
			await ctx.send(embed=embed)



		


			
	@commands.command()
	@commands.bot_has_permissions(manage_webhooks=True)
	async def mebot(self, ctx, *, msg: commands.clean_content):
		'''
		Needs permissions: manage webhooks

		Usage: sen!mebot shoto
		'''
		await ctx.message.delete()
		w = await ctx.channel.create_webhook(name=ctx.author.name)
		await w.send(msg, avatar_url=ctx.author.avatar_url)
		
		await w.delete()



	@commands.command(name='invite')
	async def invite(self, ctx):
		'''
		get invite link for the bot
		'''
		embed = discord.Embed(title="UwU you want invite me?", colour=discord.Colour(0x45487a), description="to invite me [click here](https://discordapp.com/api/oauth2/authorize?client_id=598492095682052097&permissions=8&scope=bot)")
		await ctx.send(embed=embed)






	@commands.command()
	async def minesweeper(self, ctx, size='10x10'):
		'''
		The simple and no rule minesweeper


		:param ctx:
		:param size:
		:return:
		'''
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
		'''
		Bot have a brain
		:param ctx:
		:param message:
		:return:
		'''
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
		'''
		Send invite to home server
		:param ctx:
		:return:
		'''
		await ctx.send('Home here -> **https://discord.gg/D6QyAAS**')


	@commands.command()
	async def py(self, ctx, *, kod=None):

		'''

		Run python code in sandbox
		:param ctx:
		:param kod:
		:return:
		'''
		if not kod:
			await ctx.send('Usage: ;py {code}')
			return
		message = await ctx.send(embed = discord.Embed(title='Python executor', color=discord.Colour.green(), description=f'```Waiting for response```'))
		cur_time = int(time.time())
		kod = kod.replace('```', ' ')
		kod = kod.replace('py', ' ')
		kod = kod.replace('```', ' ')
		po = {"cmd": 'python main.cpp', "src": kod}
		#r = requests.post('', data=)
		async with aiohttp.ClientSession().post('http://coliru.stacked-crooked.com/compile', data=json.dumps(po)) as res:
			r = await res.read()
		tim = int(time.time())

		res = str(r).strip('b').strip('\'').strip('\n')
		if len(res) == 0:
			res = 'No output'
		else:
			res = res[:1000]
		embed = discord.Embed(title='Python executor', color=discord.Colour.green(), description=f'```{res}```')
		embed.set_footer(text='Executed in {} seconds'.format(tim - cur_time))

		await message.edit(embed=embed)


	@commands.command()
	async def blacklist(self, ctx):
		'''
		Shows all blacklisted users


		:param ctx:
		:return:
		'''
		await ctx.send('Wait, we need to fetch all users')
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


	@commands.has_permissions(manage_channels=True)
	@commands.command()
	@commands.bot_has_permissions(manage_channels=True)
	async def setname(self, ctx, *, name=None):
		'''
		Needs permissions: manage_channels


		Set channel name (With spaces )


		:param ctx:
		:param name:
		:return:
		'''
		if not name:
			return await ctx.send(f'Usage: {ctx.prefix}set_name name')
		name = name.replace(' ', '\u2009\u2009')
		await ctx.channel.edit(name=name)
		await ctx.send('Channel updated!')
	@commands.command()
	async def embed(self, ctx: commands.Context, *, code: str=None):
		'''

		Usage: sen!embed code


		Parse code and generate a embed
		:param ctx:
		:param code:
		:return:
		'''

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
				await ctx.send(embed=embed)
			except Exception as e:
				return await ctx.send(f'In Embed Build Excpetion: {e}')

	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		'''
		Usage: sen!work

		Get some money $$$
		:param ctx:
		:return:
		'''
		coins = random.randrange(3000)
		await ctx.send(f"You worked and got {coins} coins")
		self.bot.database.add_gold(ctx.author.id, coins)
	@commands.command()
	async def translate(self, ctx: commands.Context, lang: str=None, *, text: str=None):
		'''
		Usage: sen!translate lang text

		Examples: sen!translate en привет мир
		:param ctx:
		:param lang:
		:param text:
		:return:
		'''
		if not lang or not text:
			return await ctx.send(f"""
			usage: {ctx.prefix}transtlate ru OMAEVA SINDEIRU NUNI?
			""")
		try:
			text = Translator().translate(text=text, dest=lang)
		except:
			await ctx.send('Invalid language proivded')
		embed = discord.Embed()
		embed.colour = discord.Colour.from_rgb(255,255,0)
		embed.description = f"""
		```
result: {text.text}


source: {text.src}

pronunciation: {text.pronunciation}
		```
		"""


		await ctx.send(embed=embed)



def setup(bot):        
	bot.add_cog(User(bot))
