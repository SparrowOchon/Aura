import discord
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
import typing


class UserSkills(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['upgrades', 'up', 'skill', 'skills'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def upgrade(self, ctx, upgrade: typing.Optional[str] = '', amount: typing.Optional[str] = '1'):
        member = ctx.author
        if amount == 'max':
            amount = str(9999999999999999999999999999999999999999999)
        # Adds user into the user_skill database if they are not there
        await self.client.pool.execute('''INSERT INTO user_skills(user_id, multi_hit_chance, multi_hit_factor, critical_chance, critical_power, status_chance, status_length) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''% (int(member.id), 0, 0, 0, 0, 0, 0))

        # Values
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

        # Cost
        mc_cost = 1.04**(mc_level+1)
        mf_cost = 1.04**(mf_level+1)
        cc_cost = 1.04**(cc_level+1)
        cp_cost = 1.04**(cp_level+1)

        if upgrade == 'help' or upgrade == '':
            silver_emoji = self.client.get_emoji(601632365667811369)
            points = await self.client.pool.fetchval('''SELECT POINTS FROM users WHERE user_id =%d''' % (int(member.id)))
            embed = discord.Embed(title='Skill Upgrades', description=f'Current silver: {int(points)} {silver_emoji}')
            embed.add_field(name=f'[MC] Multi-hit Chance (Level {round(mc_level)})', value=f'Chance to proc multiple messages that will also apply other upgrades. It does not proc itself. \n Chance: {round(mc_level)*0.5}% \n Cost: {round(mc_cost):,}', inline=False)
            embed.add_field(name=f'[MF] Multi-hit Factor (Level {round(mf_level)})', value=f'Number of multi-hits on proc \n Factor: {2+(mf_level)}x \n Cost: {round(mf_cost):,}', inline=False)
            embed.add_field(name=f'[CC] Critical Chance (Level {round(cc_level)})', value=f'Chance to get critical hits \n Chance: {cc_level}% \n Cost: {round(cc_cost):,}', inline=False)
            embed.add_field(name=f'[CP] Critical Power (Level {round(cp_level)})', value=f'Factor the points are multiplied by \n Factor: {2+(cp_level)}x \n Cost: {round(cp_cost):,}', inline=False)
            #embed.add_field(name=f'[SC] Status Chance (Level {sc_level})', value=f'Chance to apply a status effect, caps to certain percentage', inline=False)
            #embed.add_field(name=f'[SL] Status Length (Level {sl_level})', value=f'Length of the status effect', inline=False)
            await ctx.send(embed=embed)
        elif upgrade in mc:
            print('Upgrade multi-hit chance')
            user_points = await self.client.pool.fetchval('''SELECT points FROM users WHERE user_id = %s''' % member.id)
            if str.isdigit(amount) is True:
                # print('Upgrade initiated')
                cost_list = []
                new_level = mc_level
                if mc_cost < user_points:
                    count = 0
                    while True:
                        count = count+1
                        new_level = new_level+1
                        new_level_cost = 1.04**new_level
                        cost_list.append(new_level_cost)
                        cost_sum = sum(cost_list)
                        if cost_sum+1.04**(new_level+1) > user_points:
                            break
                        if int(count) == int(amount):
                            break
                    await self.client.pool.execute(
                        '''UPDATE users SET points = points-%s WHERE user_id = %s ''' % (
                            cost_sum, int(member.id)))
                    await self.client.pool.execute(
                        '''UPDATE user_skills SET multi_hit_chance = multi_hit_chance+%s WHERE user_id = %s ''' % (
                            count, int(member.id)))
                    await ctx.send(f'Upgraded multi-hit chance by {count} levels.')
                else:
                    await ctx.send(f'Not enough points!')
        elif upgrade in mf:
            print('Upgrade multi-hit factor')
            user_points = await self.client.pool.fetchval('''SELECT points FROM users WHERE user_id = %s''' % member.id)
            if str.isdigit(amount) is True:
                # print('Upgrade initiated')
                cost_list = []
                new_level = mf_level
                if mf_cost < user_points:
                    count = 0
                    while True:
                        count = count+1
                        new_level = new_level+1
                        new_level_cost = 1.04**new_level
                        cost_list.append(new_level_cost)
                        cost_sum = sum(cost_list)
                        if cost_sum+1.04**(new_level+1) > user_points:
                            break
                        if int(count) == int(amount):
                            break
                    await self.client.pool.execute(
                        '''UPDATE users SET points = points-%s WHERE user_id = %s ''' % (
                            cost_sum, int(member.id)))
                    await self.client.pool.execute(
                        '''UPDATE user_skills SET multi_hit_factor = multi_hit_factor+%s WHERE user_id = %s ''' % (
                            count, int(member.id)))
                    await ctx.send(f'Upgraded multi-hit factor by {count} levels.')
                else:
                    await ctx.send(f'Not enough points!')
        elif upgrade in cc:
            print('Upgrade critical chance')
            user_points = await self.client.pool.fetchval('''SELECT points FROM users WHERE user_id = %s''' % member.id)
            if str.isdigit(amount) is True:
                # print('Upgrade initiated')
                cost_list = []
                new_level = cc_level
                if cc_cost < user_points:
                    count = 0
                    while True:
                        count = count+1
                        new_level = new_level+1
                        new_level_cost = 1.04**new_level
                        cost_list.append(new_level_cost)
                        cost_sum = sum(cost_list)
                        if cost_sum+1.04**(new_level+1) > user_points:
                            break
                        if int(count) == int(amount):
                            break
                    await self.client.pool.execute(
                        '''UPDATE users SET points = points-%s WHERE user_id = %s ''' % (
                            cost_sum, int(member.id)))
                    await self.client.pool.execute(
                        '''UPDATE user_skills SET critical_chance = critical_chance+%s WHERE user_id = %s ''' % (
                            count, int(member.id)))
                    await ctx.send(f'Upgraded critical chance by {count} levels.')
                else:
                    await ctx.send(f'Not enough points!')
        elif upgrade in cp:
            print('Upgrade critical power')
            user_points = await self.client.pool.fetchval('''SELECT points FROM users WHERE user_id = %s''' % member.id)
            if str.isdigit(amount) is True:
                # print('Upgrade initiated')
                cost_list = []
                new_level = cp_level
                if cp_cost < user_points:
                    count = 0
                    while True:
                        count = count+1
                        new_level = new_level+1
                        new_level_cost = 1.04**new_level
                        cost_list.append(new_level_cost)
                        cost_sum = sum(cost_list)
                        if cost_sum+1.04**(new_level+1) > user_points:
                            break
                        if int(count) == int(amount):
                            break
                    await self.client.pool.execute(
                        '''UPDATE users SET points = points-%s WHERE user_id = %s ''' % (
                            cost_sum, int(member.id)))
                    await self.client.pool.execute(
                        '''UPDATE user_skills SET critical_power = critical_power+%s WHERE user_id = %s ''' % (
                            count, int(member.id)))
                    await ctx.send(f'Upgraded critical power by {count} levels.')
                else:
                    await ctx.send(f'Not enough points!')


def setup(client):
    client.add_cog(UserSkills(client))
