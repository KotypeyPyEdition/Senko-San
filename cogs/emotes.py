from discord.ext import commands
import discord

class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx : commands.Context, user=None):
        if not user:
            return await ctx.send("Provide user")
        user = ctx.message.mentions[0]
        if user.id == ctx.author.id:
            return await ctx.send('FOOOOOOO ')
        image = await self.image_by_tag('hug')
        embed = discord.Embed(title='Nya!', color=discord.Colour.green(), description=f'{ctx.author.mention} hugging {user.mention}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx : commands.Context, user=None):
        if not user:
            return await ctx.send("Provide user")
        user = ctx.message.mentions[0]
        if user.id == ctx.author.id:
            return await ctx.send('FOOOOOOO ')
        image = await self.image_by_tag('slap')
        embed = discord.Embed(title=':( ', color=discord.Colour.green(), description=f'{ctx.author.mention} gives a slap to {user.mention}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def baka(self, ctx : commands.Context, user=None):
        if not user:
            return await ctx.send("Provide user")
        user = ctx.message.mentions[0]
        if user.id == ctx.author.id:
            return await ctx.send('FOOOOOOO ')
        image = await self.image_by_tag('baka')
        embed = discord.Embed(title='BAKA!!1', color=discord.Colour.green(), description=f'{ctx.author.mention} saying {user.mention} is baka')
        embed.set_image(url=image)
        await ctx.send(embed=embed)



    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx : commands.Context, user=None):
        if not user:
            return await ctx.send("Provide user")
        user = ctx.message.mentions[0]
        if user.id == ctx.author.id:
            return await ctx.send('FOOOOOOO ')
        image = await self.image_by_tag('kiss')
        embed = discord.Embed(title='Nya <3', color=discord.Colour.green(), description=f'{ctx.author.mention} kiss {user.mention}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx : commands.Context, user=None):
        if not user:
            return await ctx.send("Provide user")
        user = ctx.message.mentions[0]
        if user.id == ctx.author.id:
            return await ctx.send('FOOOOOOO ')
        image = await self.image_by_tag('pat')
        embed = discord.Embed(title='Nya <3', color=discord.Colour.green(), description=f'{ctx.author.mention} patting {user.mention}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    async def image_by_tag(self, tag):
        async with self.bot.session.get('https://nekos.life/api/v2/img/' + tag) as res:
            response = await res.json()

        return response['url']



def setup(bot):
    bot.add_cog(Emotes(bot))
