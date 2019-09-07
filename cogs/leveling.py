import discord
from discord.ext import commands

import utils.database as dbu, utils.imaging


from random import randrange
from io import BytesIO


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    @commands.Cog.listener()
    async def on_message(self, msg):

        if msg.author.bot:
            return

        """
        db1 = utils.database.DBUtils()
        d = utils.imaging.ImgUtils()
        db1.create_user_profile(msg.author)
        db1.create_user_inventory(msg.author)
        stat = db1.get_user_leveling(msg.author)
        db1.create_user_socail_profile(msg.author)

        f = randrange(101)
        ff = randrange(1337)

        if f > 80:
            xp = randrange(10)
            db1.add_exp(msg.author, xp)

        if stat['xp'] >= stat['level'] * 300:
            
            dd = d.level_up_image(msg.author, stat['level'] + 1)
            
            db1.level_up(msg.author)
            db1.add_gold(msg.author, ff)
            
            emoji = discord.utils.get(self.bot.emojis, name='Gold_Nugget')
            await msg.channel.send('+ {} {}'.format(ff, str(emoji)))
            

            buffer = BytesIO()

            dd.save(
                buffer,
                "png"
            )

            buffer.seek(
                0
            )
        
        await msg.channel.send(
            fp=buffer,
            filename="profile.png"
        )
        """
            
            
            
            
            
            #f = discord.File(fp=f"temp_images/{msg.author.id}.png", filename="profile.png")
            


    

def setup(bot):
    bot.add_cog(Leveling(bot))