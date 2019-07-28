import discord
from discord.ext import commands
from discord import ChannelType
import dbl
import datetime


class Boosts(commands.Cog):
    def __init__(self, client):
        self.client = client
    #     self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3MjI2MDA2Mjc5MjEyMjM2OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY0MjQ5NjkzfQ.KHXeQJYvlm2OH9AvQ7RlIihwjfQnIsWr8q4hXK-JU6k' # set this to your DBL token
    #     self.dblpy = dbl.Client(self.client, self.token)
    #
    # async def on_dbl_vote(self, ctx):
    #     print(ctx)
    #     now = datetime.datetime.now()
    #     duration = 720 # 720 minutes = 12 hours
    #     weekend = self.dblpy.get_weekend_status()
    #     if weekend is True:
    #         factor = 3
    #     else:
    #         factor = 2
    #     await self.client.pool.execute('''INSERT INTO boosts(user_id, type, start_time, duration, factor) VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''' % (ctx.user, 'vote', now, duration, factor))


def setup(client):
    client.add_cog(Boosts(client))
