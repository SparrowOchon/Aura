from discord.ext import commands


class Boosts(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Boosts(client))
