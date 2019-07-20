import discord
from discord.ext import commands
import random


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

    @commands.command()
    async def shop(self, ctx):
        await ctx.send('Working on it!')


def setup(client):
    client.add_cog(Companion(client))
