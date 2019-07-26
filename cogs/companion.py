import discord
from discord.ext import commands
import typing
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
    async def shop(self, ctx, arg: typing.Optional[int] = 1):
        await ctx.send('Working on it!')
        if arg == 1:
            embed = discord.Embed(title='Companions', description=f'')
            await ctx.send(embed=embed)

    @commands.command()
    async def opentest(self, ctx):
        number = random.randint(1, 1000)
        if number >= 1 and number <= 900:
            await ctx.send('Common')
        elif number >= 901 and number <= 950:
            await ctx.send('Rare')
        elif number >= 951 and number <= 980:
            await ctx.send('Epic')
        elif number >= 981 and number <= 995:
            await ctx.send('Legendary')
        elif number >= 996 and number <= 1000:
            await ctx.send('Mythical')


def setup(client):
    client.add_cog(Companion(client))
