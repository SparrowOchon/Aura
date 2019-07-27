import dbl
import discord
from discord.ext import commands

import asyncio
import logging


class DiscordBotsOrgAPI(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3MjI2MDA2Mjc5MjEyMjM2OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY0MjQ5NjkzfQ.KHXeQJYvlm2OH9AvQ7RlIihwjfQnIsWr8q4hXK-JU6k' # set this to your DBL token
        self.dblpy = dbl.Client(self.client, self.token)
        self.updating = self.client.loop.create_task(self.update_stats())

    async def update_stats(self):
        while not self.client.is_closed():
            logger.info('Attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)


def setup(client):
    global logger
    logger = logging.getLogger('client')
    client.add_cog(DiscordBotsOrgAPI(client))
