import discord
from discord.ext import commands
import random
import typing


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def owner(self, ctx):
        if ctx.author.id == 153699972443799552:
            await ctx.send(f'Hello master!')
        else:
            await ctx.send(f'You\'re not my owner!')

    @commands.command()
    async def grantpoints(self, ctx, user: discord.Member = None, amount:typing.Optional[int] = 5):
        if ctx.author.id == 153699972443799552:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET points = points+%s WHERE user_id = %s' % (amount, target.id))
            await self.client.pool.execute('UPDATE users SET lifetime = lifetime+%s WHERE user_id = %s' % (amount, target.id))
            silver_emoji = self.client.get_emoji(601632365667811369)
            await ctx.send(f'{amount}{silver_emoji} granted to {target.name}')
        else:
            await ctx.send(f'You\'re not my owner!')

    @commands.command()
    async def grantflowers(self, ctx, user: discord.Member = None, amount:typing.Optional[int] = 5):
        if ctx.author.id == 153699972443799552:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET flowers = flowers+%s WHERE user_id = %s' % (amount, target.id))
            await self.client.pool.execute('UPDATE users SET lifetimeflowers = lifetimeflowers+%s WHERE user_id = %s' % (amount, target.id))
            flower_emoji = self.client.get_emoji(601881173597093912)
            await ctx.send(f'{amount}{flower_emoji} granted to {target.name}')
        else:
            await ctx.send(f'You\'re not my owner!')

    @commands.command()
    async def grantquanta(self, ctx, user: discord.Member = None, amount:typing.Optional[int] = 5):
        if ctx.author.id == 153699972443799552:
            if user:
                target = user
            else:
                target = ctx.author
            await self.client.pool.execute('UPDATE users SET quanta = quanta+%s WHERE user_id = %s' % (amount, target.id))
            quanta_emoji = self.client.get_emoji(601881165791756318)
            await ctx.send(f'{amount}{quanta_emoji} granted to {target.name}')
        else:
            await ctx.send(f'You\'re not my owner!')


def setup(client):
    client.add_cog(Admin(client))
