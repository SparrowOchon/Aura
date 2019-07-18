import discord
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
import typing


class UserSkills(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def upgrade(self, ctx, upgrade: typing.Optional[str] = '', amount: typing.Optional[str] = '1'):
        member = ctx.author

        # Adds user into the user_skill database if they are not there
        await self.client.pool.execute('''INSERT INTO user_skills(user_id, multi_hit_chance, multi_hit_factor, critical_chance, critical_power, status_chance, status_length) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''% (int(member.id), 0, 0, 0, 0, 0, 0))

        mc_level = await self.client.pool.fetchval('''SELECT multi_hit_chance FROM user_skills WHERE user_id = %s''' % member.id)
        mc = ['mc', 'multi-hit chance']
        mf_level = await self.client.pool.fetchval('''SELECT multi_hit_factor FROM user_skills WHERE user_id = %s''' % member.id)
        mf = ['mf', 'multi-hit factor']
        cc_level = await self.client.pool.fetchval('''SELECT critical_chance FROM user_skills WHERE user_id = %s''' % member.id)
        cc = ['cc', 'critical chance']
        cp_level = await self.client.pool.fetchval('''SELECT critical_power FROM user_skills WHERE user_id = %s''' % member.id)
        cp = ['cp', 'critical power']
        sc_level = await self.client.pool.fetchval('''SELECT status_chance FROM user_skills WHERE user_id = %s''' % member.id)
        sc = ['sc', 'status chance']
        sl_level = await self.client.pool.fetchval('''SELECT status_length FROM user_skills WHERE user_id = %s''' % member.id)
        sl = ['sc', 'status length']
        all_upgrades = mc + mf + cc + cp + sc + sl

        if upgrade == 'help' or upgrade == '':
            embed = discord.Embed(title='Upgrades', description='Upgrade your skills to earn more points')
            embed.add_field(name=f'[MC] Multi-hit Chance ({mc_level})', value='Chance to proc multiple messages that will also apply other upgrades', inline=False)
            embed.add_field(name=f'[MF] Multi-hit Factor ({mf_level})', value='Number of multi-hits on proc', inline=False)
            embed.add_field(name=f'[CC] Critical Chance ({cc_level})', value='Chance to get critical hits', inline=False)
            embed.add_field(name=f'[CP] Critical Power ({cp_level})', value='Factor the points are multiplied by', inline=False)
            embed.add_field(name=f'[SC] Status Chance ({sc_level})', value='Chance to apply a status effect, caps to certain percentage', inline=False)
            embed.add_field(name=f'[SL] Status Length ({sl_level})', value='Length of the status effect', inline=False)
            await ctx.send(embed=embed)

        #elif upgrade in mc:



def setup(client):
    client.add_cog(UserSkills(client))
