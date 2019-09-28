from discord.ext import commands
import hastebin
import discord
import qrcode
import io
import requests
from PIL import Image
import PIL.Image
from pytesseract import image_to_string
import pytesseract
import qrcode
import json
from utils import caesar as p
from functools import partial
class Textutils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.caes = p.Caesar()

    @commands.command(name='hastebin', aliases=['hb'])
    async def hastebin(self, ctx, text=None):
        if not text:
            await ctx.send('Usage: **;hastebin {text}**')
            return

        t = ctx.message.content.split(' ')
        del t[0]
        text = ' '.join(t)
        try:
         a = hastebin.post(text)
        except Exception as e:
         return await ctx.send("Oh, no looks hastebin server is dead please try this command later ehen server will be fixed")
        await ctx.send(embed=discord.Embed(title=f'Done you post here -> {a}'))


    @commands.command(name='reversetext', aliases=['rst', 'rt'])
    async def reverseText(self, ctx, text=None):
        if not text:
            await ctx.send('You need to privde text')
            return
        t = ctx.message.content.split(' ')
        del t[0]
        text = ' '.join(t)
        await ctx.send('Here is your text -> ```{}```'.format(text[::-1]))

    @commands.command()
    async def qr(self, ctx, *, link=None):
        if link == None:
            await ctx.send('Usage ;qr {text}')
            return
        text = link
        qr = qrcode.QRCode()
        qr.add_data(text) 
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        byte = io.BytesIO()
        img.save(byte)
        byte.seek(0)
        
        await ctx.send(file=discord.File(fp=byte, filename="a.png"))





    @commands.command(name='calc')
    async def calc(self, ctx, *, expression):
        message = await ctx.send('Trying...')
        # blacklist = ['self', 'bot', 'http', 'random', 'ctx', 'ct', 'c', 'bo', 't', 'import', 'while', 'for', 'if', 'exit(', 'eval(', 'exec()', 'self', '.', 'self.bot.http.token', 'ctx.bot.token']
        # if expression in blacklist:
        #  return await ctx.send("а не пашелка ты нахой с такими запросами?")
        allowed = '0 1 2 3 4 5 6 7 8 9 0 ( ) + - * /'
        for ch in expression:
            if not ch in allowed:
                return await ctx.send("а не пашелка ты нахой с такими запросами?")
        embed = discord.Embed(name='calc')
        try:
            po = {"cmd": 'python main.cpp', "src": f'print({expression})'}
            r = requests.post('http://coliru.stacked-crooked.com/compile', data=json.dumps(po))
            embed.colour = discord.Colour.blue()
            embed.add_field(name='Result', value=f'```{r.text}```')
        except Exception as e:
            embed.add_field(name='Result', value='Error stucked')
            embed.colour = discord.Colour.red()
            

        await ctx.send(embed=embed)

    @commands.command(name='read')
    async def image(self, ctx, url = None, lang= None):
        message = await ctx.send('> Super Senko`s image to text module is working')
        import cv2 as cv
        import numpy as np

        if not url and not ctx.message.attachments:
            await message.edit(content='> You need to put link or make an attachment with your image')
            return

        if ctx.message.attachments:
            url = ctx.message.attachments[0].url

        if lang not in ('rus', 'eng', 'ukr'):
            return await message.edit(content='> Provide language: `eng` or `rus`, `ukr`')



        b = io.BytesIO()
        img = self.fetch_image_url(url)
        img.save(b, format='PNG')
        b.seek(0)
        try:
            output = pytesseract.image_to_string(img, lang=lang)
            if len(output) == 0:
                output = 'No text found :eyes:'
            embed = discord.Embed(title='Super Senko`s read module', colour=discord.Colour.green())
            embed.add_field(name='Output', value='```{}```'.format(output))
            embed.set_footer(text='Original by TehnokraT#4879')
            await message.edit(embed=embed, content=None)
        except Exception as e:
            await message.edit(content='> Oh, no looks our reader is broken :eyes:')
        
        
        
    def fetch_image_url(self, url: str):
        r =requests.get(url)
        data = r.content
        stream = io.BytesIO(data)
        stream.seek(0)
        
        im = Image.open(stream)
        
        return im
        
def setup(bot):
    bot.add_cog(Textutils(bot))
