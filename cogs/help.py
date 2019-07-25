import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='Commands', description='')
        embed.add_field(name=f'Profile', value=f'Show your profile or someone else\'s. \nCommand: __{ctx.prefix}profile__ or __{ctx.prefix}p__')
        embed.add_field(name=f'Upgrade', value=f'Upgrade your skills. \nCommand: __{ctx.prefix}upgrade__ or __{ctx.prefix}up__')
        embed.add_field(name=f'Rebirth', value=f'Rebirth resets your stats but boosts your silver gain. \nCommand: __{ctx.prefix}rebirth__')
        embed.add_field(name=f'Leaderboards', value=f'Check the global leaderboards \nCommand: __{ctx.prefix}leaderboards__')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
