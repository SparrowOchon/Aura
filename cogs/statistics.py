import discord
from discord.ext import commands
import time


class Statistics(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Profile command
    @commands.command(aliases=['profile', 'p'])
    async def _profile(self, ctx, user: discord.Member = None):
        # Checks if an argument is provided. If there is no argument, outputs author.
        if user:
            target = user
        else:
            target = ctx.author

        # Getting the text message count of the user in the server the command was issued in
        msg_count = await self.client.pool.fetchval('''SELECT text_messages FROM users WHERE user_id =%d''' % (int(target.id),))
        # If user does not exist in the database
        if msg_count is None:
            await self.client.pool.execute(
                '''INSERT INTO users(user_id, text_messages, voice_time, points, lifetime, voice_join_timestamp) VALUES(%s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING'''
                % (int(target.id), int(0), int(0), int(0), int(0)))
        msg_count = await self.client.pool.fetchval('''SELECT text_messages FROM users WHERE user_id =%d''' % (int(target.id),))

        # Getting the voice time of the user in the server the command was issued in
        vc_count = await self.client.pool.fetchval('''SELECT voice_time FROM users WHERE user_id =%d''' % (int(target.id),))

        # Getting points
        points = await self.client.pool.fetchval('''SELECT POINTS FROM users WHERE user_id =%d''' % (int(target.id),))
        lifetime = await self.client.pool.fetchval('''SELECT lifetime FROM users WHERE user_id =%d''' % (int(target.id),))
        flowers = await self.client.pool.fetchval('''SELECT flowers FROM users WHERE user_id =%d''' % (int(target.id),))
        lifetime_flowers = await self.client.pool.fetchval('''SELECT lifetimeflowers FROM users WHERE user_id =%d''' % (int(target.id),))
        quanta = await self.client.pool.fetchval('''SELECT quanta FROM users WHERE user_id =%d''' % (int(target.id),))
        # Creating a nice looking embed
        embed = discord.Embed(title=f'Profile Information', description=f'Requested by {ctx.author}')
        # embed.add_field(name=f'Discord User ID', value=f'{target.id}', inline=False)
        embed.add_field(name=f'Text messages', value=f'{msg_count} messages', inline=False)
        vc_time = time.strftime('%H hours, %M minutes and %S seconds', time.gmtime(vc_count))
        embed.add_field(name=f'Time in voice chat', value=f'{vc_time}', inline=False)
        silver_emoji = self.client.get_emoji(601632365667811369)
        embed.add_field(name=f'Silver', value=f'{round(points):,} {silver_emoji}', inline=True)
        embed.add_field(name=f'Lifetime silver', value=f'{round(lifetime):,} {silver_emoji}', inline=True)
        flower_emoji = self.client.get_emoji(601881173597093912)
        quanta_emoji = self.client.get_emoji(601881165791756318)
        embed.add_field(name=f'Quanta', value=f'{round(quanta):,} {quanta_emoji}', inline=False)
        embed.add_field(name=f'Flower', value=f'{round(flowers):,} {flower_emoji}', inline=False)
        embed.add_field(name=f'Lifetime Flower', value=f'{round(lifetime_flowers):,} {flower_emoji}', inline=False)
        embed.set_author(name=target, icon_url=target.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Statistics(client))
