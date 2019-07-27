import discord
from discord.ext import commands
import typing
import random


class Guilds(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Guilds(client))
