import discord
from PIL import Image, ImageDraw, ImageFont
import utils.database as dbu
import requests
import io
import random
class ImgUtils:
    def __init__(self):
        self.db = dbu.DBUtils()


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



    def trigger_image(self, url):
        image = self.fetch_image_url(url)
        draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 
        width = image.size[0] #Определяем ширину. 
        height = image.size[1] #Определяем высоту. 	
        pix = image.load() #Выгружаем значения пикселей.
        depth = 10
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                a = S + depth * 2
                b = S + depth
                c = S
                a = 10
                b = b
                c = c
                draw.point((i, j), (a, b, c))

        image.save(f"temp_images/{random.randrange(9999999999)}.png", format='PNG')


    def fetch_image_url(self, url: str):
        r = requests.get(url)
        data = r.content
        stream = io.BytesIO(data)

        im = Image.open(stream)

        return im