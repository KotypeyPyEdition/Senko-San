import discord
from discord.ext import commands

import utils.database as dbu, utils.imaging


from random import randrange
from io import BytesIO


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = dbu.DBUtils(self.bot)
        


    @commands.Cog.listener()
    async def on_message(self, msg):
        
        if msg.author.bot:
            return
        self.database.register_guild_config(msg.guild)
        config = self.database.get_guild_config(msg.guild)
        db1 = utils.database.DBUtils(self.bot)
        db1.create_user_profile(msg.author.id)
        db1.register_guild_shop(msg.guild)
        stat = db1.get_user_leveling(msg.author.id)
        f = randrange(101)
        ff = randrange(100)

        if f > 80:
            xp = randrange(5)
            db1.add_exp(msg.author.id, xp)

        if stat['xp'] >= stat['level'] * 10:
            if config['lvl_msg_enabled'] == 0:
                max_gold = randrange(30)
                db1.level_up(msg.author.id)
                db1.add_gold(msg.author.id, max_gold)
                return 
            else:
                max_gold = randrange(30)
                embed = discord.Embed()
                embed.colour = discord.Colour.from_rgb(238, 249, 91)
                gold = discord.utils.get(self.bot.emojis, name='senkocoins')
                embed.title = 'Level UP!'
                embed.description = f"""
                
                
                You got {gold} {max_gold}!


                For next level you need {(stat['level'] + 1) * 10} xp to next level
                
                """
                await msg.channel.send(content=msg.author.mention, embed=embed, delete_after=15.0)
                db1.level_up(msg.author.id)
                db1.add_gold(msg.author.id, max_gold)

        
            
            
            
            
            
            #f = discord.File(fp=f"temp_images/{msg.author.id}.png", filename="profile.png")
            


    

def setup(bot):
    bot.add_cog(Leveling(bot))
