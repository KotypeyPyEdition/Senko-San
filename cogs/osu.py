from discord.ext import commands
import discord
import requests
from utils import database as ub
import utils as ii
from utils import async_client_gatari as api
import config
class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = ub.DBUtils()
        self.u = ii.util(self.bot)
        self.client = api.Client(None)
        self.utils = ii.util(self.bot)
    @commands.command(name='osu_setup')
    async def set_api_key(self, ctx):
        msg_to_del = []
        api_key = ctx.message.content.split(' ')
        if(len(api_key) == 1):
            embed = discord.Embed(title="UwU you didint provide name!", colour=discord.Colour(0x40a199), description="We need your username in game(official server) to fetch you results, scores, etc.\n Provide you username")
            self.tmp_msg = await ctx.send(embed=embed)
            msg_to_del.append(self.tmp_msg)
            return
        
        del api_key[0]
        api_key = ' '.join(api_key)
        valid = self.u.check_name_validity(api_key)
        if(valid):
            embed = discord.Embed(title="UwU that right", colour=discord.Colour(0x3ff00), description="You linked this name to your account have fun with our bot :3")
            self.tmp_msg = await ctx.send(embed=embed)
            msg_to_del.append(self.tmp_msg)
            try:
                self.db.create_profile(ctx.message.author, api_key)
            except Exception as e:
                embed = discord.Embed(title="You already registred!", colour=discord.Colour(0xff0000))
                await ctx.send(embed=embed)
                for i in msg_to_del:
                    await i.delete()
            
        else:
            embed = discord.Embed(title="i don`t know anyone with this name (c) Sagiri", colour=discord.Colour(0xff0000), description="i tryed to search you on official server but i get response `No, this man never join to server`")
            await ctx.send(embed=embed)

    @commands.command(name='osu_profile')
    async def profile(self, ctx, usr=None):
        if(len(ctx.message.content.split(' ')) == 1):
            y = self.bot.db.get_profile(ctx.message.author)
            data = self.utils.user_dict(y['osu_id'])
            SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
            SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
            S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
            Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
            A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
            self.hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
            self.hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
            self.hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
            miss = str(discord.utils.get(self.bot.emojis, name='miss'))
            embed = discord.Embed(title=f"({data['username']})\`s osu profile", colour=discord.Colour(0xb8c7e5))
            embed.add_field(name=f'{SSh_emote}' ,value=data['count_rank_ss'])
            embed.add_field(name=f'{SS_emote}' ,value=data['count_rank_ssh'])
            embed.add_field(name=f'{S_emote}' ,value=data['count_rank_sh'])
            embed.add_field(name=f'{Sh_emote}' ,value=data['count_rank_s'])
            embed.add_field(name=f'{A_emote}' ,value=data['count_rank_a'])
            embed.add_field(name='PP (raw)', value=data['pp_raw'])
            embed.add_field(name='joined at', value=data['join_date'])
            embed.add_field(name='country ', value=f" :flag_{str(data['country']).lower()}:")
            embed.add_field(name='Accuracy', value=round(float(data['accuracy']), 2))
            embed.add_field(name=f'Count of {self.hit300}', value='{} {}'.format(data['count300'], self.hit300))
            embed.add_field(name=f'Count of {self.hit100}', value='{} {}'.format(data['count100'], self.hit100))
            embed.add_field(name=f'Count of {self.hit50}', value='{} {}'.format(data['count50'], self.hit50))
            embed.add_field(name='rank of :flag_{}:'.format(str(data['country']).lower()), value='#{}'.format(data['pp_country_rank']))
            embed.add_field(name='global rank', value='#{}'.format(data['pp_rank']))
            embed.add_field(name='total score', value=data['total_score'])
            embed.add_field(name='ranked score', value=data['ranked_score'])
            embed.add_field(name='playcount', value=data['playcount'])
            embed.add_field(name='level', value=data['level'])
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            n_url = "https://a.ppy.sh/{}".format(data["user_id"])
            embed.set_thumbnail(url=n_url)
            await ctx.send(embed=embed) 
        else:
            data = self.utils.user_dict(usr)
            SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
            SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
            S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
            Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
            A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
            self.hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
            self.hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
            self.hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
            miss = str(discord.utils.get(self.bot.emojis, name='miss'))
            embed = discord.Embed(title=f"({data['username']})\`s osu profile", colour=discord.Colour(0xb8c7e5))
            embed.add_field(name=f'{SSh_emote}' ,value=data['count_rank_ss'])
            embed.add_field(name=f'{SS_emote}' ,value=data['count_rank_ssh'])
            embed.add_field(name=f'{S_emote}' ,value=data['count_rank_sh'])
            embed.add_field(name=f'{Sh_emote}' ,value=data['count_rank_s'])
            embed.add_field(name=f'{A_emote}' ,value=data['count_rank_a'])
            embed.add_field(name='PP (raw)', value=data['pp_raw'])
            embed.add_field(name='joined at', value=data['join_date'])
            embed.add_field(name='country ', value=f" :flag_{str(data['country']).lower()}:")
            embed.add_field(name='Accuracy', value=round(float(data['accuracy']), 2))
            embed.add_field(name=f'Count of {self.hit300}', value='{} {}'.format(data['count300'], self.hit300))
            embed.add_field(name=f'Count of {self.hit100}', value='{} {}'.format(data['count100'], self.hit100))
            embed.add_field(name=f'Count of {self.hit50}', value='{} {}'.format(data['count50'], self.hit50))
            embed.add_field(name='rank of :flag_{}:'.format(str(data['country']).lower()), value='#{}'.format(data['pp_country_rank']))
            embed.add_field(name='global rank', value='#{}'.format(data['pp_rank']))
            embed.add_field(name='total score', value=data['total_score'])
            embed.add_field(name='ranked score', value=data['ranked_score'])
            embed.add_field(name='playcount', value=data['playcount'])
            embed.add_field(name='level', value=data['level'])
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            n_url = "https://a.ppy.sh/{}".format(data["user_id"])
            embed.set_thumbnail(url=n_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def best(self, ctx, User=None):
        User = ctx.message.author
        y = self.bot.db.get_profile(ctx.message.author)
        data = self.utils.best_user_dict(y['osu_id'])
        data1 = self.utils.get_map(data['beatmap_id'])

        SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
        SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
        S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
        Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
        A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
        B_emote = str(discord.utils.get(self.bot.emojis, name='rank_b'))
        C_emote = str(discord.utils.get(self.bot.emojis, name='rank_c'))
        D_emote = str(discord.utils.get(self.bot.emojis, name='rank_d'))
        hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
        hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
        hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
        miss = str(discord.utils.get(self.bot.emojis, name='miss'))

        if data['rank'] == 'S':
            rank = S_emote
        elif data['rank'] == 'Sh':
            rank = Sh_emote
        elif data['rank'] == 'SS':
            rank = SS_emote
        elif data['rank'] == 'SSh':
            rank = SSh_emote
        elif data['rank'] == 'A':
            rank = A_emote
        elif data['rank'] == 'B':
            rank = B_emote
        elif data['rank'] == 'C':
            rank = C_emote
        elif data['rank'] == 'D':
            rank = D_emote
        else:
            rank = 'Undefined'
             
            
            
        embed = discord.Embed(title='Best')
        embed.color = discord.Colour.purple()
        embed.add_field(name='Beatmap name ( {}map {} )'.format(ctx.prefix, data1['beatmap_id']), value=data1['title'])
        embed.add_field(name='PP', value=round(float(data['pp'])))
        embed.add_field(name='Rank', value=rank)
        embed.add_field(name=f'Count of {hit300}', value='{} {}'.format(data['count300'], hit300))
        embed.add_field(name=f'Count of {hit100}', value='{} {}'.format(data['count100'], hit100))
        embed.add_field(name=f'Count of {hit50}', value='{} {}'.format(data['count50'], hit50))
        embed.add_field(name=f'Count of geki', value='{} {}'.format(data['countgeki'], hit100))
        embed.add_field(name=f'Count of katu', value='{} {}'.format(data['countkatu'], hit300))
        embed.add_field(name=f'Count of {miss}', value='{} {}'.format(data['countmiss'], miss))
        embed.add_field(name='Max combo', value=data['maxcombo'])
        embed.add_field(name='Score', value=data['score'])

        await ctx.send(embed=embed)


    @commands.command()
    async def last(self, ctx, User=None):
        User = ctx.message.author
        y = self.bot.db.get_profile_id(ctx.message.author.id)
        data = self.utils.user_last(y['osu_id'])
        data1 = self.utils.get_map(data['beatmap_id'])

        try:
            shtoto = data['beatmap_id']
        except Exception as e:
            await ctx.send('I cant find last play for 24 hours')
            return
        SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
        SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
        S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
        Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
        A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
        B_emote = str(discord.utils.get(self.bot.emojis, name='rank_b'))
        C_emote = str(discord.utils.get(self.bot.emojis, name='rank_c'))
        D_emote = str(discord.utils.get(self.bot.emojis, name='rank_d'))
        hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
        hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
        hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
        miss = str(discord.utils.get(self.bot.emojis, name='miss'))

        if data['rank'] == 'S':
            rank = S_emote
        elif data['rank'] == 'Sh':
            rank = Sh_emote
        elif data['rank'] == 'SS':
            rank = SS_emote
        elif data['rank'] == 'SSh':
            rank = SSh_emote
        elif data['rank'] == 'A':
            rank = A_emote
        elif data['rank'] == 'B':
            rank = B_emote
        elif data['rank'] == 'C':
            rank = C_emote
        elif data['rank'] == 'D':
            rank = D_emote
        elif data['rank'] == 'F':
            rank = 'F (No emoji)'
        else:
            rank = 'Undefined'
             
            
            
        embed = discord.Embed(title='Last')
        embed.color = discord.Colour.purple()
        embed.add_field(name='Beatmap name ( {}map {} )'.format(ctx.prefix, data1['beatmap_id']), value=data1['title'])
        embed.add_field(name='Rank', value=rank)
        embed.add_field(name=f'Count of {hit300}', value='{} {}'.format(data['count300'], hit300))
        embed.add_field(name=f'Count of {hit100}', value='{} {}'.format(data['count100'], hit100))
        embed.add_field(name=f'Count of {hit50}', value='{} {}'.format(data['count50'], hit50))
        embed.add_field(name=f'Count of geki', value='{} {}'.format(data['countgeki'], hit100))
        embed.add_field(name=f'Count of katu', value='{} {}'.format(data['countkatu'], hit300))
        embed.add_field(name=f'Count of {miss}', value='{} {}'.format(data['countmiss'], miss))
        embed.add_field(name='Max combo', value=data['maxcombo'])
        embed.add_field(name='Score', value=data['score'])
        embed.add_field(name='Osu direct (supporter only)', value="[Click here](http\:\/\/opsproject.kl.com.ua\/?map_id{})".format(data1['beatmap_id']))

        await ctx.send(embed=embed)

    @commands.command()
    async def map(self, ctx, map_id=None):
        if not map_id:
            await ctx.send('Provide map_id!')
        try:
            d = self.utils.get_map(map_id)
        except Exception as e:
            await ctx.send('This map is invalid')
            return
        

        embed = discord.Embed(title='map: {}'.format(d['title']), colour=discord.Colour(0xff56))
        embed.add_field(name='Playcount ', value=d['playcount'])
        embed.add_field(name='Passcount ', value=d['passcount'])
        embed.add_field(name='CS', value=d['diff_size'])
        embed.add_field(name='Overall', value=d['diff_overall'])
        embed.add_field(name='AR', value=d['diff_approach'])
        embed.add_field(name='OD', value=d['diff_drain'])
        embed.add_field(name='Max combo', value=d['max_combo'])
        embed.add_field(name='Artist', value=d['artist'])
        embed.add_field(name='Creator', value='Type {}osu_profile {} ({})'.format(ctx.prefix, d['creator_id'], d['creator']))
        embed.add_field(name='Osu direct (supporter only)', value="[Click here](http\:\/\/opsproject.kl.com.ua\/?map_id={})".format(d['beatmap_id']))
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)



    @commands.command()
    async def gatari_user(self, ctx: commands.Context, user=None):
        if not user:
            return await ctx.send('Provide user')

        
        data = await self.client.get_player(user)
        data2 = await self.client.get_profile(user)
        SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
        SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
        S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
        Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
        A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
        self.hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
        self.hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
        self.hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
        miss = str(discord.utils.get(self.bot.emojis, name='miss'))
        from datetime import datetime
        join_data = int(data2['registered_on'])

        join_data = datetime.utcfromtimestamp(join_data).strftime('%Y-%m-%d-%H-%M-%S')
        embed = discord.Embed(title=f"({user})\`s osu profile", colour=discord.Colour(0xb8c7e5))
        embed.add_field(name=f'{SSh_emote}' ,value=data['x_count'])
        embed.add_field(name=f'{SS_emote}' ,value=data['xh_count'])
        embed.add_field(name=f'{S_emote}' ,value=data['sh_count'])
        embed.add_field(name=f'{Sh_emote}' ,value=data['s_count'])
        embed.add_field(name=f'{A_emote}' ,value=data['a_count'])
        embed.add_field(name='PP (raw)', value=data['pp'])
        embed.add_field(name='joined at', value=join_data)
        embed.add_field(name='country ', value=f" :flag_{str(data2['country']).lower()}:")
        embed.add_field(name='Accuracy', value=round(float(data['avg_accuracy']), 2))
        embed.add_field(name='rank of :flag_{}:'.format(str(data2['country']).lower()), value='#{}'.format(data['country_rank']))
        embed.add_field(name='global rank', value='#{}'.format(data['rank']))
        embed.add_field(name='total score', value=data['total_score'])
        embed.add_field(name='ranked score', value=data['ranked_score'])
        embed.add_field(name='playcount', value=data['playcount'])
        embed.add_field(name='level', value=data['level'])
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        n_url = "https://a.gatari.pw/{}".format(data["id"])
        embed.set_thumbnail(url=n_url)
        await ctx.send(embed=embed) 


    @commands.command()
    async def gatari_best(self, ctx, user=None):
        if not user:
            await ctx.send('Provide user!')



        data1 = await self.client.get_best_user(user)
        data = data1['scores'][0]
        SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
        SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
        S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
        Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
        A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
        B_emote = str(discord.utils.get(self.bot.emojis, name='rank_b'))
        C_emote = str(discord.utils.get(self.bot.emojis, name='rank_c'))
        D_emote = str(discord.utils.get(self.bot.emojis, name='rank_d'))
        hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
        hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
        hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
        miss = str(discord.utils.get(self.bot.emojis, name='miss'))

        if data['ranking'] == 'S':
            rank = S_emote
        elif data['ranking'] == 'Sh':
            rank = Sh_emote
        elif data['ranking'] == 'x':
            rank = SS_emote
        elif data['ranking'] == 'xh':
            rank = SSh_emote
        elif data['ranking'] == 'A':
            rank = A_emote
        elif data['ranking'] == 'B':
            rank = B_emote
        elif data['ranking'] == 'C':
            rank = C_emote
        elif data['ranking'] == 'D':
            rank = D_emote
        elif data['ranking'] == 'F':
            rank = 'F (No emoji)'
        else:
            rank = 'Undefined'
             
            
        if data['full_combo']:
            is_fc = 'Yes'
        else:
            is_fc = 'No'
        embed = discord.Embed(title='Best')
        embed.color = discord.Colour.purple()
        embed.add_field(name='Beatmap name ( {}map {} )'.format(ctx.prefix, data1['scores'][0]['beatmap']['beatmap_id']), value=data1['scores'][0]['beatmap']['song_name'])
        embed.add_field(name='Rank', value=rank)
        embed.add_field(name=f'Count of {hit300}', value='{} {}'.format(data['count_300'], hit300))
        embed.add_field(name=f'Count of {hit100}', value='{} {}'.format(data['count_100'], hit100))
        embed.add_field(name=f'Count of {hit50}', value='{} {}'.format(data['count_50'], hit50))
        embed.add_field(name=f'Count of geki', value='{} {}'.format(data['count_gekis'], hit100))
        embed.add_field(name=f'Count of katu', value='{} {}'.format(data['count_katu'], hit300))
        embed.add_field(name=f'FC? ', value=is_fc)
        embed.add_field(name='Max combo', value=data['max_combo'])
        embed.add_field(name='Score', value=data['score'])
        await ctx.send(embed=embed)





    @commands.command()
    async def gatari_last(self, ctx, user=None):
        if not user:
            await ctx.send('Provide user!')



        data1 = await self.client.get_recent_user(user)
        data = data1['scores'][0]
        SSh_emote = str(discord.utils.get(self.bot.emojis, name='rank_ssp'))
        SS_emote = str(discord.utils.get(self.bot.emojis, name='rank_ss'))
        S_emote = str(discord.utils.get(self.bot.emojis, name='rank_sp'))
        Sh_emote = str(discord.utils.get(self.bot.emojis, name='rank_s'))
        A_emote = str(discord.utils.get(self.bot.emojis, name='rank_a'))
        B_emote = str(discord.utils.get(self.bot.emojis, name='rank_b'))
        C_emote = str(discord.utils.get(self.bot.emojis, name='rank_c'))
        D_emote = str(discord.utils.get(self.bot.emojis, name='rank_d'))
        hit300 = str(discord.utils.get(self.bot.emojis, name='300hit'))
        hit100 = str(discord.utils.get(self.bot.emojis, name='100hit'))
        hit50 = str(discord.utils.get(self.bot.emojis, name='50hit'))
        miss = str(discord.utils.get(self.bot.emojis, name='miss'))

        if data['ranking'] == 'S':
            rank = S_emote
        elif data['ranking'] == 'Sh':
            rank = Sh_emote
        elif data['ranking'] == 'x':
            rank = SS_emote
        elif data['ranking'] == 'xh':
            rank = SSh_emote
        elif data['ranking'] == 'A':
            rank = A_emote
        elif data['ranking'] == 'B':
            rank = B_emote
        elif data['ranking'] == 'C':
            rank = C_emote
        elif data['ranking'] == 'D':
            rank = D_emote
        elif data['ranking'] == 'F':
            rank = 'F (No emoji)'
        else:
            rank = 'Undefined'
             
            
        if data['full_combo']:
            is_fc = 'Yes'
        else:
            is_fc = 'No'
        embed = discord.Embed(title='Last')
        embed.color = discord.Colour.purple()
        embed.add_field(name='Beatmap name ( {}map {} )'.format(ctx.prefix, data1['scores'][0]['beatmap']['beatmap_id']), value=data1['scores'][0]['beatmap']['song_name'])
        embed.add_field(name='Rank', value=rank)
        embed.add_field(name=f'Count of {hit300}', value='{} {}'.format(data['count_300'], hit300))
        embed.add_field(name=f'Count of {hit100}', value='{} {}'.format(data['count_100'], hit100))
        embed.add_field(name=f'Count of {hit50}', value='{} {}'.format(data['count_50'], hit50))
        embed.add_field(name=f'Count of geki', value='{} {}'.format(data['count_gekis'], hit100))
        embed.add_field(name=f'Count of katu', value='{} {}'.format(data['count_katu'], hit300))
        embed.add_field(name=f'FC? ', value=is_fc)
        embed.add_field(name='Max combo', value=data['max_combo'])
        embed.add_field(name='Score', value=data['score'])
        await ctx.send(embed=embed)
        




def setup(bot):
    bot.osu_token = config.osu_token
    bot.add_cog(Osu(bot))
