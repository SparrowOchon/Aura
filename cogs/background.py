import discord
from discord.ext import tasks, commands
from discord import ChannelType
import random
import datetime


class Background(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_check.start()

    def cog_unload(self):
        self.voice_check.cancel()

    @tasks.loop(seconds=15)
    async def voice_check(self):
        for guild in list(self.client.guilds):
            # print('Checking guilds')
            voice_channels = (vc for vc in guild.channels if vc.type == ChannelType.voice)
            for voice in voice_channels:
                users = voice.members
                if voice.members is None:
                    break
                else:
                    for member in users:
                        # Adds user to the database if they are not in it
                        await self.client.pool.execute(
                            '''INSERT INTO users(user_id, text_messages, voice_time, points, lifetime, voice_join_timestamp) VALUES(%s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING''' % (
                            int(member.id), int(0), int(0), int(0), int(0)))
                        # Get the time in voice chat
                        now = datetime.datetime.now()
                        before_timestamp = await self.client.pool.fetchval(
                            '''SELECT voice_join_timestamp FROM users WHERE user_id = %s''' % (member.id))
                        if before_timestamp is None:
                            # print('Adding new timestamp')
                            await self.client.pool.execute(
                                '''UPDATE users SET voice_join_timestamp = $$%s$$ WHERE user_id = %s''' % (
                                    now, member.id))
                            before_timestamp = now
                        td = now - before_timestamp
                        td_seconds = int(td.total_seconds())
                        # print(td_seconds)
                        await self.client.pool.execute(
                            '''UPDATE users SET voice_time = voice_time + %s WHERE user_id = %s''' % (
                            td_seconds, member.id))
                        hits = round(td_seconds / 30)
                        # print(hits)

                        # Retrieves levels
                        mc_level = await self.client.pool.fetchval(
                            '''SELECT multi_hit_chance FROM user_skills WHERE user_id = %s''' % member.id)
                        mc = ['mc', 'multi-hit chance']
                        mf_level = await self.client.pool.fetchval(
                            '''SELECT multi_hit_factor FROM user_skills WHERE user_id = %s''' % member.id)
                        mf = ['mf', 'multi-hit factor']
                        cc_level = await self.client.pool.fetchval(
                            '''SELECT critical_chance FROM user_skills WHERE user_id = %s''' % member.id)
                        cc = ['cc', 'critical chance']
                        cp_level = await self.client.pool.fetchval(
                            '''SELECT critical_power FROM user_skills WHERE user_id = %s''' % member.id)
                        cp = ['cp', 'critical power']
                        sc_level = await self.client.pool.fetchval(
                            '''SELECT status_chance FROM user_skills WHERE user_id = %s''' % member.id)
                        sc = ['sc', 'status chance']
                        sl_level = await self.client.pool.fetchval(
                            '''SELECT status_length FROM user_skills WHERE user_id = %s''' % member.id)
                        sl = ['sc', 'status length']

                        # Points per message
                        ppm = 1
                        points = 0

                        while True:
                            if hits == 0:
                                break
                            hits = hits - 1
                            print(f'Checking voice time of {member.name}')
                            # Calculates multi-hit
                            multi_chance = mc_level * 0.5
                            multi_factor = 2 + (mf_level)
                            multi_hits = 0
                            if multi_chance > 100:
                                # print('Multi-hit chance above 100!')
                                while True:
                                    multi_chance = multi_chance - 100
                                    multi_hits = multi_hits + 1
                                    if multi_chance < 100:
                                        break
                            if random.randint(1, 100) < multi_chance:
                                multi_hits = multi_hits + 1

                            multi_msg = multi_hits * multi_factor
                            # print(f'Multi hits {multi_hits}')
                            # print(f'Multi factor {multi_factor}')
                            # print(f'Multi_msg {multi_msg}')
                            msg = multi_msg + 1
                            # print(f'Message count: {msg}')
                            # Calculates critical hits
                            critical_chance = cc_level * 1
                            critical_hits = 0
                            critical_power = cp_level + 2
                            if critical_chance > 100:
                                while True:
                                    critical_chance = critical_chance - 100
                                    critical_hits = critical_hits + 1
                                    if critical_chance < 100:
                                        break
                            # print(f'CC {critical_chance}%')
                            while True:
                                msg = msg - 1
                                hit = 0
                                if random.randint(1, 100) < critical_chance:
                                    # print('Critical proc!')
                                    hit = 1
                                    points = points + critical_power * ppm
                                else:
                                    points = points + ppm
                                if msg == 0:
                                    break
                            # Calculating points
                            # print(f'CH {critical_hits}')
                            if int(critical_hits) > 0:
                                # print('Critical hits detected')
                                points = points * critical_hits * critical_power * ppm
                            if hits == 0:
                                break

                            lifetime_flowers = await self.client.pool.fetchval(
                                '''SELECT lifetimeflowers FROM users WHERE user_id =%d''' % (int(member.id),))
                            flowers_boost = 1 + float(lifetime_flowers) * 0.001
                            points = points * flowers_boost

                            print(f'Points {round(points):,} to {member.name} for voice chat')
                            # Adds points to the database
                            await self.client.pool.execute(
                                '''UPDATE users SET points = points+%s WHERE user_id = %s ''' % (
                                points, int(member.id)))
                            # Adds lifetime points to the database
                            await self.client.pool.execute(
                                '''UPDATE users SET lifetime = lifetime+%s WHERE user_id = %s ''' % (
                                points, int(member.id)))
                            # Store the current timestamp in the database
                            now = datetime.datetime.now()
                            await self.client.pool.execute(
                                '''UPDATE users SET voice_join_timestamp = $$%s$$ WHERE user_id = %s''' % (
                                now, member.id))
                            if hits == 0:
                                break

    @voice_check.before_loop
    async def before_voice_check(self):
        # print('Loop is waiting')
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Background(client))
