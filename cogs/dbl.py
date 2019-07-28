import dbl
import discord
from discord.ext import commands

import asyncio
import logging


class DiscordBotsOrgAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI3MjI2MDA2Mjc5MjEyMjM2OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY0MjQ5NjkzfQ.KHXeQJYvlm2OH9AvQ7RlIihwjfQnIsWr8q4hXK-JU6k' # set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='gryphticon123', webhook_port=5000)
        self.updating = self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while not self.bot.is_closed():
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
        print(data)
        voter_id = data.get('user', '')
        print(voter_id)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))