import discord
from discord.ext import commands
import time
import typing
import asyncpg


class Statistics(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Profile command
    @commands.command(aliases=['profile', 'p'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _profile(self, ctx, user: discord.Member = None):
        # Checks if an argument is provided. If there is no argument, outputs author.
        if user:
            target = user
        else:
            target = ctx.author

        # Getting the text message count of the user in the server the command was issued in
        msg_count = await self.client.pool.fetchval('''SELECT text_messages FROM users WHERE user_id =%d''' % (int(target.id),))
        # If user does not exist in the database
        if msg_count is None:
            await self.client.pool.execute(
                '''INSERT INTO users(user_id, text_messages, voice_time, points, lifetime, voice_join_timestamp) VALUES(%s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING'''
                % (int(target.id), int(0), int(0), int(0), int(0)))
        msg_count = await self.client.pool.fetchval('''SELECT text_messages FROM users WHERE user_id =%d''' % (int(target.id),))

        # Getting the voice time of the user in the server the command was issued in
        vc_count = await self.client.pool.fetchval('''SELECT voice_time FROM users WHERE user_id =%d''' % (int(target.id),))

        # Getting points
        points = await self.client.pool.fetchval('''SELECT POINTS FROM users WHERE user_id =%d''' % (int(target.id),))
        lifetime = await self.client.pool.fetchval('''SELECT lifetime FROM users WHERE user_id =%d''' % (int(target.id),))
        flowers = await self.client.pool.fetchval('''SELECT flowers FROM users WHERE user_id =%d''' % (int(target.id),))
        lifetime_flowers = await self.client.pool.fetchval('''SELECT lifetimeflowers FROM users WHERE user_id =%d''' % (int(target.id),))
        quanta = await self.client.pool.fetchval('''SELECT quanta FROM users WHERE user_id =%d''' % (int(target.id),))
        rebirths = await self.client.pool.fetchval('''SELECT rebirth FROM users WHERE user_id =%d''' % (int(target.id),))
        # Creating a nice looking embed
        embed = discord.Embed(title=f'', description=f'')
        # embed.add_field(name=f'Discord User ID', value=f'{target.id}', inline=False)
        embed.add_field(name=f'Text messages', value=f'{msg_count} messages', inline=False)
        vc_time = time.strftime('%H hours, %M minutes and %S seconds', time.gmtime(vc_count))
        # print(str(target.avatar_url))
        embed.set_thumbnail(url=target.avatar_url)
        embed.add_field(name=f'Time in voice chat', value=f'{vc_time}', inline=False)
        silver_emoji = self.client.get_emoji(601632365667811369)
        embed.add_field(name=f'Silver', value=f'{round(points):,} {silver_emoji}', inline=True)
        embed.add_field(name=f'Lifetime silver', value=f'{round(lifetime):,} {silver_emoji}', inline=True)
        # embed.add_field(name=f'\u200b', value=f'\u200b', inline=True)
        flower_emoji = self.client.get_emoji(601881173597093912)
        quanta_emoji = self.client.get_emoji(601881165791756318)
        embed.add_field(name=f'Flower', value=f'{round(flowers):,} {flower_emoji}', inline=True)
        embed.add_field(name=f'Lifetime Flower', value=f'{round(lifetime_flowers):,} {flower_emoji}', inline=True)
        embed.add_field(name=f'Rebirths', value=f'{rebirths}', inline=True)
        embed.add_field(name=f'Quanta', value=f'{round(quanta):,} {quanta_emoji}', inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.set_author(name=target, icon_url=target.avatar_url)
        await ctx.send(embed=embed)

    # Leaderboards command
    @commands.command(aliases=['lb', 'leaderboard', 'leaderboards'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _leaderboard(self, ctx, number: typing.Optional[int] = 1, currency_type: typing.Optional[str] = 'silver'):
        silver_aliases = [
            'silver',
            'points',
            'point',
            's'
        ]
        lifetime_silver_aliases = [
            'lifetimesilver',
            'lifetimepoints',
            'lifetimepoint',
            'ls',
            'lifetime'
        ]
        flower_aliases = [
            'flower',
            'flowers',
            'rebirth'
        ]
        lifetime_flower_aliases = [
            'lifetimeflower',
            'lifetimeflowers',
            'lifetimerebirth',
            'lf'
        ]
        currency = 'silver'
        name = 'silver'
        if currency_type in silver_aliases:
            currency = 'points'
            title = 'Silver'
        elif currency_type in flower_aliases:
            currency = 'flowers'
            name = 'flowers'
            title = 'Flowers'
        elif currency_type in lifetime_silver_aliases:
            currency = 'lifetime'
            name = 'lifetime silver'
            title = 'Lifetime Silver'
        elif currency_type in lifetime_flower_aliases:
            currency = 'lifetimeflowers'
            name = 'lifetime flowers'
            title = 'Lifetime Flowers'

        points = await self.client.pool.fetch('''SELECT %s FROM users ORDER BY %s DESC OFFSET %s ROWS FETCH FIRST 10 ROWS ONLY''' % (currency, currency, (number*10-10)))
        user_id = await self.client.pool.fetch('''SELECT user_id FROM users ORDER BY %s DESC OFFSET %s ROWS FETCH FIRST 10 ROWS ONLY''' % (currency, (number*10-10)))
        iteration = 0
        embed = discord.Embed(title=f'{title} Leaderboards', description=f'Page {number}')
        embed.set_footer(text=f"Requested by {ctx.author}")
        for users in user_id:
            uid = user_id[iteration]
            cur = points[iteration]
            user_id_value = uid['user_id']
            points_value = cur[f'{currency}']
            user = self.client.get_user(user_id_value)
            if user is None:
                username = f'Anonymous User'
            else:
                username = user.name
            embed.add_field(name=f'#{int(iteration)+int(1)+int(number*10-10)} - {username}', value=f'{int(points_value):,} {name}', inline=False)
            iteration = iteration+1
            if iteration == 10:
                break
        await ctx.send(embed=embed)

    # Leaderboards command
    @commands.command(aliases=['glb', 'guildleaderboard', 'guildleaderboards', 'slb', 'serverleaderboard', 'serverleaderboards'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _guildleaderboard(self, ctx, number: typing.Optional[int] = 1, currency_type: typing.Optional[str] = 'silver'):
        silver_aliases = [
            'silver',
            'points',
            'point',
            's'
        ]
        lifetime_silver_aliases = [
            'lifetimesilver',
            'lifetimepoints',
            'lifetimepoint',
            'ls',
            'lifetime'
        ]
        flower_aliases = [
            'flower',
            'flowers',
            'rebirth'
        ]
        lifetime_flower_aliases = [
            'lifetimeflower',
            'lifetimeflowers',
            'lifetimerebirth',
            'lf'
        ]
        currency = 'silver'
        name = 'silver'
        if currency_type in silver_aliases:
            currency = 'points'
            title = 'Silver'
        elif currency_type in flower_aliases:
            currency = 'flowers'
            name = 'flowers'
            title = 'Flowers'
        elif currency_type in lifetime_silver_aliases:
            currency = 'lifetime'
            name = 'lifetime silver'
            title = 'Lifetime Silver'
        elif currency_type in lifetime_flower_aliases:
            currency = 'lifetimeflowers'
            name = 'lifetime flowers'
            title = 'Lifetime Flowers'

        points = await self.client.pool.fetch('''SELECT %s FROM users WHERE EXISTS(SELECT 1 FROM guild_members WHERE users.user_id = guild_members.user_id AND guild_members.guild_id = %s) ORDER BY %s DESC OFFSET %s ROWS FETCH FIRST 10 ROWS ONLY''' % (currency, ctx.guild.id, currency, (number*10-10)))
        user_id = await self.client.pool.fetch('''SELECT user_id FROM users WHERE EXISTS(SELECT 1 FROM guild_members WHERE users.user_id = guild_members.user_id AND guild_members.guild_id = %s) ORDER BY %s DESC OFFSET %s ROWS FETCH FIRST 10 ROWS ONLY''' % (ctx.guild.id, currency, (number*10-10)))
        iteration = 0
        embed = discord.Embed(title=f'{title} Leaderboards in {ctx.guild.name}', description=f'Page {number}')
        embed.set_footer(text=f"Requested by {ctx.author}")
        for users in user_id:
            uid = user_id[iteration]
            cur = points[iteration]
            user_id_value = uid['user_id']
            points_value = cur[f'{currency}']
            user = self.client.get_user(user_id_value)
            if user is None:
                username = f'Anonymous User'
            else:
                username = user.name
            embed.add_field(name=f'#{int(iteration)+int(1)+int(number*10-10)} - {username}', value=f'{int(points_value):,} {name}', inline=False)
            iteration = iteration+1
            if iteration == 10:
                break
        await ctx.send(embed=embed)

    # Info command
    @commands.command(aliases=['info', 'information', 'i'])
    async def _info(self, ctx):
        await ctx.send('Working on it')

    @commands.command()
    async def guilds(self, ctx, number: typing.Optional[int] = '1'):
        if ctx.author.id == 153699972443799552:
            guild_list = list(self.client.guilds)
            embed = discord.Embed(title=f'Aura Guild List')
            iteration = 0
            for guild in guild_list:
                iteration = iteration+1
                embed.add_field(name=f'{int(iteration)}. {guild.name}', value=f'{guild.member_count} members', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('I only serve Gryphticon')


def setup(client):
    client.add_cog(Statistics(client))
