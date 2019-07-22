import discord
from discord.ext import commands
import random
import typing
import math


class Rebirth(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rebirth(self, ctx, confirm: typing.Optional[str] = ''):
        member = ctx.author
        lifetime = await self.client.pool.fetchval('''SELECT lifetime FROM users WHERE user_id =%d''' % (int(member.id),))
        lifetime_flowers = await self.client.pool.fetchval('''SELECT lifetimeflowers FROM users WHERE user_id =%d''' % (int(member.id),))
        flowers = int((1/2000)*math.sqrt(int(lifetime)))
        if confirm == 'yes':
            await ctx.send('You have been reborn')
            embed = discord.Embed(title='Rebirth', description='')
            silver_emoji = self.client.get_emoji(601632365667811369)
            flower_emoji = self.client.get_emoji(601881173597093912)
            embed.add_field(name='Lifetime silver', value=f'{round(lifetime):,} {silver_emoji}', inline=True)
            # embed.add_field(name='Conversion rate', value=f'{round(inverse_rate):,} {silver_emoji} per {flower_emoji}', inline=True)
            embed.add_field(name='Flowers from rebirth', value=f'{round(flowers):,} {flower_emoji}', inline=False)
            embed.add_field(name='Previous Boost Factor', value=f'{round(1+(float(lifetime_flowers))*0.001):,}x', inline=True)
            embed.add_field(name='Current Boost Factor', value=f'{round(1+(flowers+float(lifetime_flowers))*0.001):,}x', inline=True)
            await ctx.send(embed=embed)
            # Give flowers
            await self.client.pool.execute('UPDATE users SET lifetimeflowers = lifetimeflowers+%s WHERE user_id = %s' % (flowers, member.id))
            await self.client.pool.execute('UPDATE users SET flowers = flowers+%s WHERE user_id = %s' % (flowers, member.id))
            # Reset
            await self.client.pool.execute('UPDATE users SET lifetime = 0 WHERE user_id = %s' % member.id)
            await self.client.pool.execute('UPDATE users SET points = 0 WHERE user_id = %s' % member.id)
            await self.client.pool.execute('UPDATE user_skills SET multi_hit_chance = 0 WHERE user_id = %s' % member.id)
            await self.client.pool.execute('UPDATE user_skills SET multi_hit_factor = 0 WHERE user_id = %s' % member.id)
            await self.client.pool.execute('UPDATE user_skills SET critical_chance = 0 WHERE user_id = %s' % member.id)
            await self.client.pool.execute('UPDATE user_skills SET critical_power = 0 WHERE user_id = %s' % member.id)
        elif confirm == 'help':
            await ctx.send('Rebirth resets only your silver and upgrades. Lifetime flowers multiply your silver gain.')
        else:
            embed = discord.Embed(title='Rebirth Preview', description='')
            silver_emoji = self.client.get_emoji(601632365667811369)
            flower_emoji = self.client.get_emoji(601881173597093912)
            embed.add_field(name='Lifetime silver', value=f'{round(lifetime):,} {silver_emoji}', inline=True)
            embed.add_field(name='Flowers from rebirth', value=f'{round(flowers):,} {flower_emoji}', inline=False)
            embed.add_field(name='Current Boost Factor', value=f'{round(1+(float(lifetime_flowers))*0.001):,}x', inline=True)
            embed.add_field(name='Final Boost Factor', value=f'{round(1+(flowers+float(lifetime_flowers))*0.001):,}x', inline=True)
            await ctx.send(embed=embed)
            await ctx.send(f'Use the command \'{ctx.prefix}rebirth yes\' to rebirth.')


def setup(client):
    client.add_cog(Rebirth(client))
