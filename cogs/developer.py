import discord
from discord.ext import commands
import random


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def owner(self, ctx):
        if ctx.author.id == 153699972443799552:
            await ctx.send(f'Hello master!')
        else:
            await ctx.send(f'You\'re not my owner!')


def setup(client):
    client.add_cog(Admin(client))
