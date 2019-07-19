import discord
from discord.ext import commands
import random


class Rebirth(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rebirth(self, ctx):
        member = ctx.author


def setup(client):
    client.add_cog(Rebirth(client))
