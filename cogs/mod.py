from discord.ext import commands
import discord
import asyncio
from utils import database
class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = database.DBUtils(self.bot)



    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
        if not member:
            await ctx.send("Provide user")
        if member.id == ctx.message.author.id or member.id == ctx.message.guild.me.id:
            await ctx.send('You can`t ban me or youself or roles! ')
            return
        if member.top_role.position >= ctx.message.guild.me.top_role.position:
            await ctx.send('Her role is highter than my! i can`t ban he')
            return
        if not reason:
            reason = 'None'
        else:
            reason = reason

        embed = discord.Embed(title='Confirmation', description='Ok, ill ban {} with reason `{}` \n if you agree press ✅'.format(member.name, reason))
        embed.color = 0x32a852

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❎')
        try:
            r, u = await self.bot.wait_for('reaction_add', check=lambda r,u: u.id == ctx.message.author.id, timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.send('Timed out!')
        else:
            if str(r) == '✅':
                await member.send(f"You banned at {ctx.guild.name} with reason {reason} by {ctx.author.name}")
                await ctx.message.guild.ban(member, reason=reason, delete_message_days=7)
                await ctx.send('Im banned {} with reason `{}` good luck :)'.format(f'<@{member.id}>', reason))
            else:
                await ctx.send('canceled')
                return
                #

    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await ctx.send('Provide user')
            return
        if member.id == ctx.message.author.id or member.id == ctx.message.guild.me.id:
                await ctx.send('You can`t kick me or youself or roles! ')
                return
        if member.top_role.position >= ctx.message.guild.me.top_role.position:
                await ctx.send('Her role is highter than my! i can`t kick he')
                return
        reason = ctx.message.content.split(' ')
        if not reason:
                reason = 'None'
            
        embed = discord.Embed(title='Confirmation', description='Ok, ill kick {} with reason `{}` \n if you agree press ✅'.format(member.name, reason))
        embed.color = 0x32a852
            
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❎')
        try:
            r, u = await self.bot.wait_for('reaction_add', check=lambda r,u: u.id == ctx.message.author.id and r.message.id == message.id, timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.send('Timed out!')
        else:
            if str(r) == '✅':
                await ctx.message.guild.kick(member, reason=reason)
                await ctx.send('Im kicked {} with reason `{}` good luck :)'.format(f'<@{member.id}>', reason))
            else:
                await ctx.send('canceled')
                return

    @commands.command(name='clear')
    @commands.has_permissions(read_message_history=True, manage_messages=True)
    async def clear(self, ctx: commands.Context, amout=None):
        cur_lang = await self.bot.redis.get('{ctx.guild.id}_lang')
        cur_lang = str(cur_lang.strip('b\''))
        channel = ctx.message.channel
        if amout == None:
            await ctx.send(self.bot.language.get_message(f'{cur_lang}.clear_cmd_provide_msg_amout'))
            return
        if int(amout) > 100:
            return await ctx.send(self.bot.language.get_message(f'{cur_lang}.clear_cmd_max_limit'))
        


        await ctx.channel.purge(amout)
        await ctx.send(self.bot.language.get_message(f'{cur_lang}.clear_cmd_max_limit'))
 

    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user=None, *, reason=None):
      import discord
      if not user and not reason:
      	return await ctx.send("Usage: ;mute @user#1234 reason why we lose")
      elif not ctx.message.mentions:
      	return await ctx.send("Please mention user")
      try:
      	mentions = ctx.message.mentions[0]
      	usr = await ctx.guild.fetch_member(mentions.id)
      except Exception as e:
      	return await ctx.send("Looks this user is not in guild")
      
      overwrite = discord.PermissionOverwrite()
      overwrite.send_messages = False
      overwrite.add_reactions = False
      for i in ctx.guild.channels:
      	await i.set_permissions(usr, overwrite=overwrite)

      await ctx.send("Okay, {} muted with reason `{}`".format(usr.name, reason))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user=None):
      import discord
      if not user:
      	return await ctx.send("Usage: ;unmute @user#1234 reason why we lose")
      elif not ctx.message.mentions:
      	return await ctx.send("Please mention user")
      try:
      	mentions = ctx.message.mentions[0]
      	usr = await ctx.guild.fetch_member(mentions.id)
      except Exception as e:
      	return await ctx.send("Looks this user is not in guild")
      for i in ctx.guild.channels:
      	await i.set_permissions(usr, overwrite=None)

      await ctx.send("Okay, now {} can talk".format(usr.name))



    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def language(self, ctx: commands.Context, lang=None):
        cur_lang =  await str(self.bot.redis.get('{ctx.guild.id}_lang'))
        cur_lang = cur_lang.strip('b\'')
        await ctx.send(cur_lang)
        if not lang:
            res = await str(self.bot.redis.get('{ctx.guild.id}_lang'))
            res = res.strip('b\'')

            msg = self.bot.language.get_message('{cur_lang}.curent_lang').format(res)
            return await ctx.send(f'{msg}')

        if lang not in  await self.bot.language.get_languages():
            msg = self.bot.language.get_message(f'{cur_lang}.available_langs').format(', '.join(self.bot.language.get_languages()))
            return await ctx.send(msg)
        
        await self.bot.redis.set(f'{ctx.guild.id}_lang', lang)
        update_msg = self.bot.language.get_message(f'{cur_lang}.settings_updated')
        await ctx.send(update_msg)

        

def setup(bot):
    bot.add_cog(Mod(bot))
