import discord
from PIL import Image, ImageDraw, ImageFont
import utils.database as dbu
import io
import random
from functools import partial
class ImgUtils:
    def __init__(self, bot):
        self.bot = bot
        self.db = dbu.DBUtils(bot)


    def level_up_image(self, user: discord.User, lvl: int):
        lvl_up = Image.open('image_tools/lvl_up_template.png')
        font = ImageFont.truetype("image_tools/font.ttf", 30)
        d = self.fetch_image_url(str(user.avatar_url_as(format='png')) + "?size=64")
        d.resize((16, 16))
        drow = ImageDraw.Draw(lvl_up)
        lvl_up.paste(d, (10,10))
        drow.text((140, 70), 'Level UP', font=font)
        drow.text((10, 150), 'You are now {} level'.format(lvl), font=font)
        
        return lvl_up


    async def profile_image(self, user: discord.User) -> bytes:
        a = io.BytesIO()
        dd = await self.db.get_user_leveling(user)
        desc = await self.db.get_user_desc(user)

        with Image.open("image_tools/template.png") as res:
            drow = ImageDraw.Draw(img)
            user_avatar = await self.fetch_image_url(user.avatar_url_as(format='png', size=64))
            im2 = Image.open(user_avatar)
		#await ctx.send(str(ctx.message.author.avatar_url_as(format='png')) + "?size=64x64")
            font = ImageFont.truetype("image_tools/font.ttf", 25)
            desc_font = ImageFont.truetype("image_tools/desc_font.ttf", 20)
            user_desc = textwrap.fill(desc, width=17)
            drow.text((200, 245), user.name, font=font)
            drow.text((60, 300), 'level: ', font=font)
            drow.text((130, 300), str(dd['level']), font=font)
            drow.text((60, 350), 'xp: ', font=font)
            drow.text((100, 350), str(dd['xp']) + "/" + str(dd['level']*300) , font=font)
            drow.text((60, 400), 'gold: ', font=font)
            drow.text((120, 400), str(dd['gold']) , font=font)
            drow.text((280, 315), user_desc , font=desc_font)
            
        
            img.save(a, format='PNG')
        a.seek(0)
        return a

    async def fetch_image_url(self, url: str) -> bytes:
        async with self.bot.session.get(url) as res:
            data = await res.read()


        return data
