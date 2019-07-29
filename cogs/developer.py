import datetime
import typing

import discord
from discord.ext import commands


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.gm = [
            153699972443799552,
            184103737369952256
        ]


    @commands.command()
    async def owner(self, ctx):
        if ctx.author.id == 153699972443799552:
            await ctx.send(f'Hello master!')
        else:
            await ctx.send('I only serve Gryphticon')

    # Currency Commands

    @commands.command()
    async def grantpoints(self, ctx, user: discord.Member = None, amount: typing.Optional[int] = 5):
        if ctx.author.id in self.client.gm:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET points = points+%s WHERE user_id = %s' % (amount, target.id))
            await self.client.pool.execute('UPDATE users SET lifetime = lifetime+%s WHERE user_id = %s' % (amount, target.id))
            silver_emoji = self.client.get_emoji(601632365667811369)
            await ctx.send(f'{amount}{silver_emoji} granted to {target.name}')
        else:
            self.ctx.send('I only serve Gryphticon')

    @commands.command()
    async def grantflowers(self, ctx, user: discord.Member = None, amount: typing.Optional[int] = 5):
        if ctx.author.id in self.client.gm:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET flowers = flowers+%s WHERE user_id = %s' % (amount, target.id))
            await self.client.pool.execute('UPDATE users SET lifetimeflowers = lifetimeflowers+%s WHERE user_id = %s' % (amount, target.id))
            flower_emoji = self.client.get_emoji(601881173597093912)
            await ctx.send(f'{amount}{flower_emoji} granted to {target.name}')
        else:
            self.ctx.send('I only serve Gryphticon')

    @commands.command()
    async def grantquanta(self, ctx, user: discord.Member = None, amount: typing.Optional[int] = 5):
        if ctx.author.id in self.client.gm:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET quanta = quanta+%s WHERE user_id = %s' % (amount, target.id))
            quanta_emoji = self.client.get_emoji(601881165791756318)
            await ctx.send(f'{amount}{quanta_emoji} granted to {target.name}')
        else:
            self.ctx.send('I only serve Gryphticon')

    @commands.command()
    async def reset(self, ctx, user: discord.Member = None):
        if ctx.author.id in self.client.gm:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute(
                'UPDATE users SET flowers = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE users SET lifetimeflowers = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE users SET points = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE users SET lifetime = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE user_skills SET multi_hit_chance = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE user_skills SET multi_hit_factor = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE user_skills SET critical_chance = 0 WHERE user_id = %s' % target.id)
            await self.client.pool.execute(
                'UPDATE user_skills SET critical_power = 0 WHERE user_id = %s' % target.id)
            await ctx.send(f'{target.name}\'s progress was reset!')

        else:
            await ctx.send('I only serve Gryphticon')

    @commands.command()
    async def populate(self, ctx):
        if ctx.author.id in self.client.gm:
            everyone = await self.client.pool.fetchval(
                '''SELECT user_id FROM users''')
            for member in everyone:
                await self.client.pool.execute(
                    '''INSERT INTO guild_members(user_id, guild_id) VALUES(%s, %s) ON CONFLICT DO NOTHING''' % (
                    int(member.id), ctx.author.guild.id))
                await ctx.send('Guild leaderboards have been populated')
        else:
            await ctx.send('I only serve Gryphticon')

    # Boost Commands

    @commands.command()
    async def givevoteboost(self,ctx, user: discord.Member = None):
        if ctx.author.id in self.client.gm:
            if user:
                target = user
            else:
                target = ctx.author
        now = datetime.datetime.now()
        duration = 720 # 720 minutes = 12 hours
        factor = 2
        await self.client.pool.execute('''INSERT INTO boosts(user_id, type, start_time, duration, factor) VALUES($$%s$$, $$%s$$, $$%s$$, $$%s$$, $$%s$$)''' % (target.id, 'vote', now, duration, factor))
        await ctx.send(f'Vote boost was given to {target.display_name}')

    @commands.command()
    async def checkboosts(self, ctx, user: discord.Member = None):

        await self.client.pool.execute('DELETE FROM boosts WHERE make_interval(mins := duration) < now()-start_time''')

    # Pet commands

    @commands.command()
    async def givepet(self, ctx):
        await ctx.send('WIP')

def setup(client):
    client.add_cog(Developer(client))
