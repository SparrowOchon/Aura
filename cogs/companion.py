import discord
from discord.ext import commands
import typing


class Companion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx, user: discord.Member = None):
        # Checks if an argument is provided. If there is no argument, outputs author.
        if user:
            target = user
        else:
            target = ctx.author
        img = 'https://i.imgur.com/0crAHkT.gif'
        embed = discord.Embed(title=f'Testing stuff, {target.name}!')
        embed.set_image(url=f'{img}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['pet', 'pets'])
    async def _pets(self, arg:typing.Optional[str] = '', selection=''):
        await self.ctx.send('Working on it!')
        if arg == '':
            embed = discord.Embed(title='Companions', description='')


def setup(client):
    client.add_cog(Companion(client))
