import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dab(self, ctx, user: discord.Member = None):
        # Checks if an argument is provided. If there is no argument, outputs author.
        if user:
            target = user
        else:
            target = ctx.author
        dab_images = [
            'https://i.imgur.com/Y0ZfhYv.jpg',
            'https://i.imgur.com/f2IRUHh.jpg',
            'https://i.imgur.com/dTztqJ8.jpg',
            'https://i.imgur.com/VcRn48o.jpg',
            'https://i.imgur.com/MFLFhw3.png',
            'https://i.imgur.com/HXtHTAa.jpg',
            'https://i.imgur.com/VEjxXxs.png',
            'https://i.imgur.com/5IgMBvG.jpg',
            'https://i.imgur.com/pvAHzhs.png',
            'https://i.imgur.com/jWWZxGs.jpg',
            'https://i.imgur.com/zMH9scJ.png',
            'https://i.imgur.com/zzkJABQ.png',
            'https://i.imgur.com/X38QE3L.png',
            'https://i.imgur.com/X95Ejv1.jpg',
            'https://i.imgur.com/DLzJvAH.jpg'
        ]
        embed = discord.Embed(title=f'Get dabbed on {target.name}!')
        embed.set_image(url=f'{random.choice(dab_images)}')
        await ctx.send(embed=embed)

    @commands.command()
    async def bilo(self, ctx):
        await ctx.send('Bilo is noob')


def setup(client):
    client.add_cog(Fun(client))
