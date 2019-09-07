from nekos import nekos
from discord.ext import commands
import discord

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.is_nsfw()
    @commands.command()
    async def neko(self, ctx, *, tag=None):
        possible = [
            'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
            'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
            'ngif', 'meow', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
            'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
            'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
            'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
            'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
            'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
            'smallboobs', 'hug', 'ero'
        ]
        embed = discord.Embed(title='Error', color=0xff0033)
        embed.add_field(name='Enter a tag possible:', value='`' + ', '.join(possible) + '`')
        if not tag or tag not in possible:
            await ctx.send(embed=embed)
            return
        
        res = nekos.img(tag)
        embed2 = discord.Embed(name=None, color=0x65cf65)
        embed2.set_image(url=res)
        await ctx.send(embed=embed2)
        

def setup(bot):
    bot.add_cog(Nsfw(bot))
