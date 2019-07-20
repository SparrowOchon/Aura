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
        embed = discord.Embed(title=f'Get dabbed on {target.name}!')
        embed.set_image(url=f'{img}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Companion(client))
