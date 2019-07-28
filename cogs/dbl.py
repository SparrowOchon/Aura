import asyncio
import datetime
import logging

import dbl
from discord.ext import commands


class DiscordBotsOrgAPI(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3MjI2MDA2Mjc5MjEyMjM2OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY0MjQ5NjkzfQ.KHXeQJYvlm2OH9AvQ7RlIihwjfQnIsWr8q4hXK-JU6k' # set this to your DBL token
        self.dblpy = dbl.Client(self.client, self.token, webhook_path='/dblwebhook', webhook_auth='gryphticon123', webhook_port=5000)
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

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        logger.info('Received an upvote')
        voter_id = data.get('user', '')
        now = datetime.datetime.now()
        duration = 720 # 720 minutes = 12 hours
        weekend = await self.dblpy.get_weekend_status()
        if weekend is True:
            factor = 3
        else:
            factor = 2
        await self.client.pool.execute('''INSERT INTO boosts(user_id, type, start_time, duration, factor) VALUES($$%s$$, $$%s$$, $$%s$$, %s, %s) ON CONFLICT DO NOTHING''' % (int(voter_id), 'vote', now, duration, factor))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        logger.info('Received an upvote')
        voter_id = data.get('user', '')
        now = datetime.datetime.now()
        duration = 720 # 720 minutes = 12 hours
        weekend = await self.dblpy.get_weekend_status()
        if weekend is True:
            factor = 3
        else:
            factor = 2
        await self.client.pool.execute('''INSERT INTO boosts(user_id, type, start_time, duration, factor) VALUES($$%s$$, $$%s$$, $$%s$$, %s, %s) ON CONFLICT DO NOTHING''' % (int(voter_id), 'vote', now, duration, factor))


def setup(client):
    global logger
    logger = logging.getLogger('client')
    client.add_cog(DiscordBotsOrgAPI(client))
