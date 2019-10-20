from discord.ext import commands
import discord
import asyncio
from utils import database
from main import SenkoSanBot
class Mod(commands.Cog):
    def __init__(self, bot: SenkoSanBot):
        self.bot = bot



    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
        if not member:
            await ctx.send("Provide user")
        if ctx.author.top_role.position > member.top_role.position:
            return await ctx.send('Ehm... its Trolling or what?')
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
    async def kick(self, ctx: commands.Context, member: discord.Member=None, *, reason=None):
        if not member:
            await ctx.send('Provide user')
            return
        if ctx.author.top_role.position > member.top_role.position:
            return await ctx.send('Ehm... its Trolling or what?')
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
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def mute(self, ctx, user: discord.Member=None, *, reason=None):
        
        
        if not user and not reason:
            return await ctx.send("Usage: ;mute @user#1234 reason why we lose")
        if user.id == ctx.guild.me.id:
            return await ctx.send('I now can not just take and seal my mouth with tape')
        if ctx.author.top_role.position < user.top_role.position:
            return await ctx.send('Ehm... its Trolling or what?')
        if user.id == ctx.author.id:
            return await ctx.send('Suicide - not an option')
        mute_role = discord.utils.get(ctx.guild.roles, name='senko mute')
        if not mute_role:
            msg = await ctx.send('I can not find mute role, create it?')
            await msg.add_reaction('✅')
            try:
                r, u = await self.bot.wait_for('reaction_add', check=lambda r, u: r.message.id == msg.id and u.id == ctx.author.id, timeout=60)
            except asyncio.TimeoutError as e:
                return await ctx.send('Canceled')
            else:
                if str(r) == '✅':
                    m_role = await ctx.guild.create_role(name='senko mute')
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    overwrite.add_reactions = False
                    for i in ctx.guild.channels:
                        await i.set_permissions(m_role, overwrite=overwrite)
                    await ctx.send('I created and overwrited permissions')
                    await user.add_roles(m_role, reason=f'Mute by {ctx.author.name}, reason: {reason}')
                    await ctx.send(f'{user.mention} has been muted by {ctx.author.mention}, with reason: {reason}')
                    try: await user.send(f'You have been muted in guild {ctx.guild.name}, by {ctx.author.mention} with reason {reason}')
                    except: pass
                    return
                else:
                  return await ctx.send('canceled')



        await user.add_roles(mute_role, reason=f'Mute by {ctx.author.name}, reason: {reason}')
        await ctx.send(f'{user.mention} has been muted by {ctx.author.mention}, with reason: {reason}')
        try: await user.send(f'You have been muted in guild {ctx.guild.name}, by {ctx.author.mention} with reason {reason}')
        except: pass


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member=None):
        if not user:
            return await ctx.send('usage: sen!unmute @user#1234')
        
        mute_role = discord.utils.get(ctx.guild.roles, name='senko mute')
        if not mute_role:
            return await ctx.send('This server does not even have the mute role, that you want to do about it?')
        if mute_role not in user.roles:
            return await ctx.send('This member may have to say, what is it all about?')
        await user.remove_roles(mute_role)
        await ctx.send('I unmuted {}'.format(user.mention))
        try: await user.send('You have been unmuted in guild {} by {}'.format(ctx.guild.name, ctx.author.mention))
        except: pass
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def guild_config(self, ctx: commands.Context):
        res = self.bot.database.get_guild_config(ctx.guild)
        help_ = """
        disable LUP messages: `;guild_config lup_msgs 0`
        
        0 - disabled
        1 - enabled
        """
        lup_emoji = discord.utils.get(self.bot.emojis, name='Xp_bottle')
        if res['lvl_msg_enabled'] == 0:
            lup = f'No!, press {str(lup_emoji)} to enable'
        else:
            lup = f'Yes!, press {str(lup_emoji)} to disable'
        embed_builder = discord.Embed()
        embed_builder.colour = discord.Color.from_rgb(252, 248, 3)
        embed_builder.add_field(name='Level UP! messages enabled', value=lup)
        msg = await ctx.send(embed=embed_builder)
        await msg.add_reaction(lup_emoji)
        try:
            r,u = await self.bot.wait_for('reaction_add', check=lambda r,u: r.message.id == msg.id and u.id == ctx.author.id, timeout=60)
        except asyncio.TimeoutError as e:
            pass

        else:
            if str(r) == '<:Xp_bottle:602455920659922944>':
                if res['lvl_msg_enabled'] == 0:
                    self.bot.database.set_lvlup_msg(ctx.guild, 1)
                    await ctx.send('> Level UP! messages has been enabled')
                else:
                    self.bot.database.set_lvlup_msg(ctx.guild, 0)
                    await ctx.send('> Level UP! messages has been disabled')

    @commands.command()
    async def shop(self, ctx: commands.Context, item: int=None):
        if not item:
            shop = self.bot.database.get_role_shop(ctx.guild)
            if len(shop) == 0:
                shop = 'There is nothing for sale'
                return await ctx.send(shop)
            embed = discord.Embed()
            l = []
            counter = 0
            for i in shop:
                counter += 1
                role = ctx.guild.get_role(i['role'])
                l.append(f"**{counter}** | {role.mention} : {i['cost']}")
            embed.description = '\n'.join(l)
            embed.set_footer(text='To buy use sen!shop {counter}')
            return await ctx.send(embed=embed)
        
        shop = self.bot.database.get_role_shop(ctx.guild)
        itm = {}
        counter = 0
        for i in shop:
            counter += 1
            itm[counter] = i
        if item not in itm:
            return await ctx.send('there is no role in the store!')
        item = itm[item]

        data = self.bot.database.get_user_leveling(ctx.author.id)
        if int(item['cost']) > int(data['gold']):
            return await ctx.send('do not have enough gold')
        try:
            role = ctx.guild.get_role(item['role'])
            if role in ctx.author.roles:
                return await ctx.send('you already have this role, what are you hoping for?')
            self.bot.database.add_gold(ctx.author.id, -int(item['cost']))
            await ctx.author.add_roles(role)
            await ctx.send(f'You bought {role.name} role')
        except:
            await ctx.send('Something went wrong... maybe i don`t have permissions to give roles?')
        



    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def addrole(self,ctx,role: discord.Role=None, cost=None):
        if not role or not cost:
            return await ctx.send("usage: sen!addrole @role 6")
        if role.position > ctx.author.top_role.position:
            await ctx.send('Backdoor is closed!')
        if role.position >= ctx.message.guild.me.top_role.position:
            return await ctx.send("i can't give this role anyone")
        if int(cost) < 0:
            return await ctx.send("Cost must can't be negative")
        shop = self.bot.database.get_role_shop(ctx.guild)
        a = {}
        for i in shop:
            a[i['role']] = i['cost']
        if role.id in a:
            return await ctx.send('this role is already in the store, what you hoped?')
        self.bot.database.add_shop_role(ctx.guild, role, cost)
        await ctx.send("Done!")


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def removerole(self, ctx: commands.Context, role: discord.Role=None):
        if not role:
            return await ctx.send(f'usage: {ctx.prefix}removerole @role1')
        shop = self.bot.database.get_role_shop(ctx.guild)
        embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,0))
        a = {}
        for i in shop:
            a[i['role']] = i['cost']
        if role.id not in a:
            return await ctx.send('this role and so is not in the store, what are you hoping for?')
        self.bot.database.remove_shop_role(ctx.guild, role)
        await ctx.send('Done!')

        

def setup(bot):
    bot.add_cog(Mod(bot))
