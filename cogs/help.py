import typing

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['help', 'command', 'commands'])
    async def _help(self, ctx, cmd: typing.Optional[str] = ''):
        if cmd == '':
            embed = discord.Embed(title='Commands', description=f'Use \"{ctx.prefix}help [command]\" to learn more about each commands. \n e.g. \"{ctx.prefix}help profile\"')
            embed.add_field(name=f'Economy', value=f'`upgrade`, `rebirth`, `vote`')
            embed.add_field(name=f'Statistics', value=f'`profile`, `leaderboards`, `guildleaderboards`')
            embed.add_field(name=f'Server Admin', value=f'`prefix`')
            if ctx.author.id == 153699972443799552:
                embed.add_field(name=f'Developer', value=f'`grantpoints`, `grantflowers`, `grantquanta`, `reset`, `populate`, `givevoteboost`, `checkboosts`')
            embed.add_field(name=f'Miscellaneous', value=f'`dab`, `screenshare`')
            await ctx.send(embed=embed)
        elif cmd in ['upgrade', 'upgrades']:
            embed = discord.Embed(title='Upgrade', description='Use this command to upgrade your skills and further upgrade your point gain')
            embed.add_field(name=f'Check available upgrades', value=f'Use \"{ctx.prefix}upgrade\" to view all available upgrades')
            embed.add_field(name=f'Upgrading a skill', value=f'Use \"{ctx.prefix}upgrade skill number\" to view all available upgrades. You can substitute the number for max to buy the maximum upgrades you can afford. \n e.g. \"{ctx.prefix}upgrade mc 10\"')
            await ctx.send(embed=embed)
        elif cmd == 'rebirth':
            embed = discord.Embed(title='Rebirth', description=f'Use this command to reset all your silver and upgrades to gain an overall silver boost. \n Use \"{ctx.prefix}rebirth\" for more information (running this command will not rebirth you).')
            await ctx.send(embed=embed)
        elif cmd == 'profile':
            embed = discord.Embed(title='Profile', description=f'Use this command to look at your profile or someone else\'. \n Write \"{ctx.prefix}profile\" to view your own profile. \nUse \"{ctx.prefix}profile @mention\" to view someone else\'s profile.')
            await ctx.send(embed=embed)
        elif cmd == 'prefix':
            embed = discord.Embed(title='Prefix', description=f'Change the prefix on your server. Only the server-owner can change the prefix. \n Write \"{ctx.prefix}prefix newprefix\" to change the prefix on your server.')
            await ctx.send(embed=embed)
        elif cmd == 'dab':
            embed = discord.Embed(title='Dab', description='Dab like a madman')
            await ctx.send(embed=embed)
        elif cmd in ['screenshare', 'share', 'screen', 'sharescreen']:
            embed = discord.Embed(title='Screen sharing', description='Use this command while in a voice channel to produce a link that allows you to display or view screenshares. Everyone who wants to see the screenshare must click on the link.')
            await ctx.send(embed=embed)
        elif cmd in ['leaderboards', 'lb', 'leaderboard']:
            embed = discord.Embed(title='Leaderboards', description=f'The page number and currency are optional. Using {ctx.prefix}leaderboards will yield the top 10 for silver.')
            embed.add_field(name=f'Aliases',value=f'`lb`, `leaderboard`, `leaderboards`')
            await ctx.send(embed=embed)
        elif cmd in ['guildleaderboards', 'glb', 'guildleaderboard']:
            embed = discord.Embed(title='Guild Leaderboards', description=f'The page number and currency are optional. Using {ctx.prefix}guildleaderboards will yield the top 10 for silver.')
            embed.add_field(name=f'Aliases',value=f'`glb`, `guildleaderboard`, `guildleaderboards`')
            await ctx.send(embed=embed)
        elif cmd in ['vote', 'voteboost', 'votehelp']:
            embed = discord.Embed(title='Vote for the bot and receive a silver boost!', description='')
            embed.add_field(name='Vote here', value='https://discordbots.org/bot/272260062792122368/vote')
            embed.add_field(name='Rates', value='2x boost on weekdays \n 3x boost on weekends')
            await ctx.send(embed=embed)
        else:
            await ctx.send('Command not found, please check your spelling.')

    @commands.command(aliases=['vote', 'voteboost', 'votehelp'])
    async def _vote_help(self, ctx):
        embed = discord.Embed(title='Vote for the bot and receive a silver boost!', description='')
        embed.add_field(name='Vote here', value='https://discordbots.org/bot/272260062792122368/vote')
        embed.add_field(name='Rates', value='2x boost on weekdays \n 3x boost on weekends', inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
