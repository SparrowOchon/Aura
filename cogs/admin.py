import discord
from discord.ext import commands
import random


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, *, arg):
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == 153699972443799552:
            member = ctx.author
            await self.client.pool.execute('UPDATE guilds SET prefix = $$%s$$ WHERE guild_id = %s' % (str(arg), ctx.guild.id))
            await ctx.send(f'{ctx.guild.name} prefix changed to {arg}')
            print('Prefix changed')
        else:
            await ctx.send(f'Only the server owner, {ctx.guild.owner.name}, can change the prefix.')


def setup(client):
    client.add_cog(Admin(client))
