from discord.ext import commands
import discord
import asyncio
from utils import database
class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = database.DBUtils()



    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx):
        if len(ctx.message.mentions) == 0:
            await ctx.send('Provide user')
            return
        member = ctx.message.mentions[0]
        if str(ctx.prefix) == '<@{}>'.format(ctx.guild.me.id):
            member = ctx.message.mentions[1]
        if member.id == ctx.message.author.id or member.id == ctx.message.guild.me.id:
            await ctx.send('You can`t ban me or youself or roles! ')
            return
        if member.bot == True:
            await ctx.send('Дайте ботам свободу уже!!!')
            return
        if member.top_role.position >= ctx.message.guild.me.top_role.position:
            await ctx.send('Her role is highter than my! i can`t ban he')
            return
        reason = ctx.message.content.split(' ')
        del reason[0]
        del reason[0]
        del reason[0]
        if len(reason) == 0:
            reason = 'None'
        else:
            reason = ' '.join(reason)

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
                await ctx.message.guild.ban(member, reason=reason, delete_message_days=7)
                await ctx.send('Im banned {} with reason `{}` good luck :)'.format(f'<@{member.id}>', reason))
            else:
                await ctx.send('canceled')
                return
                #

    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx):
        if len(ctx.message.mentions) == 0:
            await ctx.send('Provide user')
            return
        member = ctx.message.mentions[0]
        if str(ctx.prefix) == '<@{}>'.format(ctx.guild.me.id):
                member = ctx.message.mentions[1]
        if member.id == ctx.message.author.id or member.id == ctx.message.guild.me.id:
                await ctx.send('You can`t kick me or youself or roles! ')
                return
        if member.bot == True:
                await ctx.send('Дайте ботам свободу уже!!!')
                return
        if member.top_role.position >= ctx.message.guild.me.top_role.position:
                await ctx.send('Her role is highter than my! i can`t kick he')
                return
        reason = ctx.message.content.split(' ')
        del reason[0]
        del reason[0]
        del reason[0]
        if len(reason) == 0:
                reason = 'None'
        else:
                reason = ' '.join(reason)
            
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
    async def clear(self, ctx, amout=None, member=None):
        if amout == None:
            await ctx.send('Provide amout of messages!(max 100)')
            return
        if int(amout) > 100:
            await ctx.send('Maximum discord limit is 100 i can`t delete more than 100 messages')
            return
        channel = ctx.message.channel
        ments = ctx.message.mentions
        msgs = []
        if len(ments) == 0:
            async for i in channel.history(limit=int(amout)):
                msgs.append(i)

            await ctx.channel.purge(limit=len(msgs))
        else:
            a = ctx.message.mentions[0]
            if str(ctx.prefix) == '<@{}>'.format(ctx.guild.me.id):
                    a = ctx.message.mentions[1]
            async for i in channel.history(limit=int(amout)):
                if i.author.id == a.id:
                    msgs.append(i)
            await ctx.channel.purge(limit=len(msgs), check=lambda m: m.author.id == a.id)

        
        await ctx.send('UwU! im deletet {} messages'.format(len(msgs)))
 

    
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
   


        
def setup(bot):
    bot.add_cog(Mod(bot))
