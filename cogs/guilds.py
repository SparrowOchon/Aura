import discord
from discord.ext import commands
import typing
import random


class Guilds(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_guild_join(self, guild):
        channel = self.client.get_channel(604741076900642826)
        await self.client.pool.execute('''INSERT INTO guilds(guild_id, prefix, count) VALUES(%s, $$%s$$, %s) ON CONFLICT DO NOTHING''' % (int(guild.id), '.', int(guild.member_count)))
        await channel.sent(f'{guild.name} added {self.client.user.name}')


def setup(client):
    client.add_cog(Guilds(client))
