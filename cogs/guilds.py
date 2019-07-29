import typing

import discord
from discord.ext import commands


class Guilds(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_guild_join(self, guild):
        channel = self.client.get_channel(604741076900642826)
        await self.client.pool.execute('''INSERT INTO guilds(guild_id, prefix, count) VALUES(%s, $$%s$$, %s) ON CONFLICT DO NOTHING''' % (int(guild.id), '.', int(guild.member_count)))
        await channel.sent(f'{guild.name} with {guild.member_count} members added {self.client.user.name}')

    @commands.command(aliases=['enlistguild', 'enlistserver', 'guildenlist', 'serverenlist'])
    async def _enlistguild(self, ctx, confirm: typing.Optional[str] = ''):
        if ctx.message.author.id != ctx.guild.owner.id or ctx.author.id != 153699972443799552:
            await ctx.send(f'Only the server owner, {ctx.guild.owner.name}, can enlist the server as a guild')
            return
        if confirm == '':
            embed = discord.Embed(title=f'Enlist {ctx.guild.name}', description='')
            embed.add_field(name='What does enlisting do?', value='Enlisting your server as a guild will allow you to compete with other guilds. As your guild progresses, your members gain bonuses when they participate in your server.')
            embed.add_field(name='How to enlist', value=f'If you wish to enlist, please write `{ctx.prefix}enlistguild yes`.')
            await ctx.send(embed=embed)
        elif confirm == 'yes':
            guild_id = ctx.guild.id
            await self.client.pool.execute('''INSERT INTO enlisted_guilds(guild_id, boost, xp, level) VALUES (%s, %s, %s, %s)''' % (guild_id, 0, 0, 0))
            await ctx.send(f'{ctx.guild.name} has been enlisted as a guild.')

    @commands.command(aliases=['guild', 'server'])
    async def _guild(self, ctx, screen: typing.Optional[str] = '', number: typing.Optional[str] = ''):
        if screen in ['', 'info', 'i']:
            # Showing the guild profile screen
            guild_db = await self.client.pool.fetchrow('''SELECT * FROM enlisted_guilds WHERE guild_id = %s''' % ctx.guild.id)
            if guild_db is None:
                if ctx.message.author.id != ctx.guild.owner.id or ctx.author.id != 153699972443799552:
                    await ctx.send(f'{ctx.guild.name} is not enlisted as a guild! Please do `{ctx.prefix}enlistguild` for more information.')
                else:
                    await ctx.send(f'{ctx.guild.name} is not enlisted as a guild! Please ask {ctx.guild.owner.name} to do `{ctx.prefix}enlistguild` for more information.')
            embed = discord.Embed(title=f'{ctx.guild.name} Guild Profile')
            xp = guild_db['xp']
            embed.add_field(name='XP', value=f'{xp} XP', inline=False)
            levels = guild_db['level']
            embed.add_field(name='Level', value=f'{levels}', inline=False)
            boost = guild_db['boost']
            embed.add_field(name='Boost', value=f'{boost+1}x', inline=False)
        else:
            await ctx.send('Command not recognized.')


def setup(client):
    client.add_cog(Guilds(client))
