import discord
from discord.ext import commands
import random
import typing


class Rebirth(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rebirth(self, ctx, confirm: typing.Optional[str] = ''):
        member = ctx.author
        if confirm == 'confirm':
            await ctx.send('You have been reborn')
        else:
            await ctx.send(f'Use the command \'{ctx.prefix}rebirth confirm\' to rebirth.')


def setup(client):
    client.add_cog(Rebirth(client))
