import discord
import os
from discord.ext import commands
import asyncio
import asyncpg
import logging
import datetime
import random


# Logs to console
logging.basicConfig(level=logging.INFO)

token = 'MjcyNTAzNTMxMDIwMzUzNTM2.XTIOPg.XSaDU9PGLis92rJhQQ6SdODMS8A'


# Database Operations
async def create_db_pool():
    client.pool = await asyncpg.create_pool(host='127.0.0.1', database='GameBot', user='postgres', password='admin123')

    # Creates the user database
    await client.pool.execute('''CREATE TABLE IF NOT EXISTS users( 
                        user_id BIGINT,
                        text_messages INTEGER,
                        voice_time INTEGER,
                        points DECIMAL,
                        lifetime DECIMAL,
                        voice_join_timestamp TIMESTAMP,
                        PRIMARY KEY(user_id))''')

    # Creates the user skill database
    await client.pool.execute('''CREATE TABLE IF NOT EXISTS user_skills( 
                        user_id BIGINT,
                        multi_hit_chance BIGINT,
                        multi_hit_factor BIGINT,
                        critical_chance BIGINT,
                        critical_power BIGINT,
                        status_chance BIGINT,
                        status_length BIGINT,
                        PRIMARY KEY(user_id))''')

    # Creates the guild database
    await client.pool.execute('''CREATE TABLE IF NOT EXISTS guilds( 
                            guild_id BIGINT,
                            prefix TEXT,
                            PRIMARY KEY(guild_id))''')

    # New additions

    # Rebirth Currency (users)
    await client.pool.execute('''ALTER TABLE users ADD COLUMN IF NOT EXISTS flowers DECIMAL DEFAULT 0''')

    # Premium Currency (users)
    await client.pool.execute('''ALTER TABLE users ADD COLUMN IF NOT EXISTS quanta DECIMAL DEFAULT 0''')


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or('.')(bot, message)
    prefix = await client.pool.fetchval('SELECT prefix FROM guilds WHERE guild_id = %s' % message.guild.id)
    print(prefix)
    if prefix is None:
        return commands.when_mentioned_or('.')(bot, message)
    return commands.when_mentioned_or(str(prefix))(bot, message)


client = commands.Bot(command_prefix=get_prefix)

# Loop to look through cogs folder and load all cogs contained within it
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # splicing cuts 3 last characters aka .py
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    member = message.author

    # Add users into the database if they're not there
    await client.pool.execute('''INSERT INTO users(user_id, text_messages, voice_time, points, lifetime, voice_join_timestamp) VALUES(%s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING''' % (int(member.id), int(0), int(0), int(0), int(0)))

    # Adds user into the user_skill database if they are not there
    await client.pool.execute(
        '''INSERT INTO user_skills(user_id, multi_hit_chance, multi_hit_factor, critical_chance, critical_power, status_chance, status_length) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''' % (
        int(member.id), 0, 0, 0, 0, 0, 0))

    # Adds the text message to the database
    await client.pool.execute('''UPDATE users SET text_messages = text_messages+1 WHERE user_id = %s ''' % (int(member.id)))

    # Retrieves levels
    mc_level = await client.pool.fetchval(
        '''SELECT multi_hit_chance FROM user_skills WHERE user_id = %s''' % member.id)
    mc = ['mc', 'multi-hit chance']
    mf_level = await client.pool.fetchval(
        '''SELECT multi_hit_factor FROM user_skills WHERE user_id = %s''' % member.id)
    mf = ['mf', 'multi-hit factor']
    cc_level = await client.pool.fetchval(
        '''SELECT critical_chance FROM user_skills WHERE user_id = %s''' % member.id)
    cc = ['cc', 'critical chance']
    cp_level = await client.pool.fetchval(
        '''SELECT critical_power FROM user_skills WHERE user_id = %s''' % member.id)
    cp = ['cp', 'critical power']
    sc_level = await client.pool.fetchval(
        '''SELECT status_chance FROM user_skills WHERE user_id = %s''' % member.id)
    sc = ['sc', 'status chance']
    sl_level = await client.pool.fetchval(
        '''SELECT status_length FROM user_skills WHERE user_id = %s''' % member.id)
    sl = ['sc', 'status length']

    # Points per message
    ppm = 1
    points = 0

    # Calculates multi-hit
    multi_chance = mc_level*0.5
    multi_factor = (mf_level+1)*2
    multi_hits = 0
    if multi_chance > 100:
        print('Multi-hit chance above 100!')
        while True:
            multi_chance = multi_chance-100
            multi_hits = multi_hits+1
            if multi_chance < 100:
                break
    if random.randint(1, 100) < multi_chance:
        multi_hits = multi_hits+1

    multi_msg = multi_hits*multi_factor
    # print(f'Multi hits {multi_hits}')
    # print(f'Multi factor {multi_factor}')
    # print(f'Multi_msg {multi_msg}')
    msg = multi_msg+1
    # print(f'msg {msg}')
    # Calculates critical hits
    critical_chance = cc_level*1
    critical_hits = 0
    critical_power = (cp_level+1)*2
    if critical_chance > 100:
        while True:
            critical_chance = critical_chance-100
            critical_hits = critical_hits+1
            if critical_chance < 100:
                break
    while True:
        msg = msg-1
        total_crit = critical_hits
        if random.randint(1,100) < critical_chance:
            # print('Crit proc!')
            critical_hits = critical_hits+1
            points = points+(critical_hits)*critical_power*ppm
        else:
            points = points+ppm
        if msg == 0:
            break

    print(f'Points {points}')
    # Adds points to the database
    await client.pool.execute('''UPDATE users SET points = points+%s WHERE user_id = %s ''' % (points, int(member.id)))
    # Adds lifetime points to the database
    await client.pool.execute(
        '''UPDATE users SET lifetime = lifetime+%s WHERE user_id = %s ''' % (points, int(member.id)))

    # Print the message
    print(f'{message.author} in {message.guild.name}: {message.content}')
    await client.process_commands(message)


@client.event
async def on_voice_state_update(member, before, after):

    # User joined the channel
    if before.channel is None and after.channel is not None:
        print(member, 'joined ', after.channel, ' in ', member.guild.name)

        # Adds user to the database if they are not in it
        await client.pool.execute(
            '''INSERT INTO users(user_id, text_messages, voice_time, points, lifetime, voice_join_timestamp) VALUES(%s, %s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING''' % (int(member.id), int(0), int(0), int(0), int(0)))

        # Store the current timestamp in the database
        now = datetime.datetime.now()
        await client.pool.execute('''UPDATE users SET voice_join_timestamp = $$%s$$ WHERE user_id = %s''' % (now, member.id))

    # User left the channel
    if before.channel is not None and after.channel is None:
        print(member, 'left ', before.channel, ' in ', member.guild.name)
        if member.guild.afk_channel is None or before.channel.id is not member.guild.afk_channel.id:

            # Get the time in voice chat
            before_timestamp = await client.pool.fetchval('''SELECT voice_join_timestamp FROM users WHERE user_id = %s''' % (member.id))
            now = datetime.datetime.now()
            td = now - before_timestamp
            td_seconds = int(td.total_seconds())
            print(td_seconds)
            await client.pool.execute('''UPDATE users SET voice_time = voice_time + %s WHERE user_id = %s''' % (td_seconds, member.id))

            hits = round(td_seconds/30)
            while True:
                if hits == 0:
                    break
                hits = hits-1
                # Adds user into the user_skill database if they are not there
                await client.pool.execute(
                    '''INSERT INTO user_skills(user_id, multi_hit_chance, multi_hit_factor, critical_chance, critical_power, status_chance, status_length) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''' % (
                        int(member.id), 0, 0, 0, 0, 0, 0))

                # Retrieves levels
                mc_level = await client.pool.fetchval(
                    '''SELECT multi_hit_chance FROM user_skills WHERE user_id = %s''' % member.id)
                mc = ['mc', 'multi-hit chance']
                mf_level = await client.pool.fetchval(
                    '''SELECT multi_hit_factor FROM user_skills WHERE user_id = %s''' % member.id)
                mf = ['mf', 'multi-hit factor']
                cc_level = await client.pool.fetchval(
                    '''SELECT critical_chance FROM user_skills WHERE user_id = %s''' % member.id)
                cc = ['cc', 'critical chance']
                cp_level = await client.pool.fetchval(
                    '''SELECT critical_power FROM user_skills WHERE user_id = %s''' % member.id)
                cp = ['cp', 'critical power']
                sc_level = await client.pool.fetchval(
                    '''SELECT status_chance FROM user_skills WHERE user_id = %s''' % member.id)
                sc = ['sc', 'status chance']
                sl_level = await client.pool.fetchval(
                    '''SELECT status_length FROM user_skills WHERE user_id = %s''' % member.id)
                sl = ['sc', 'status length']

                # Points per message
                ppm = 1
                points = 0

                # Calculates multi-hit
                multi_chance = mc_level * 0.5
                multi_factor = (mf_level + 1) * 2
                multi_hits = 0
                if multi_chance > 100:
                    print('Multi-hit chance above 100!')
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
                # Calculates critical hits
                critical_chance = cc_level * 1
                critical_hits = 0
                critical_power = (cp_level + 1) * 2
                if critical_chance > 100:
                    while True:
                        critical_chance = critical_chance - 100
                        critical_hits = critical_hits + 1
                        if critical_chance < 100:
                            break
                while True:
                    msg = msg - 1
                    total_crit = critical_hits
                    if random.randint(1, 100) < critical_chance:
                        # print('Crit proc!')
                        total_crit = total_crit + 1
                    points = points + ppm * (total_crit + 1) * critical_power
                    if msg == 0:
                        break
                if hits == 0:
                    break

                print(f'Points {points}')
                # Adds points to the database
                await client.pool.execute(
                    '''UPDATE users SET points = points+%s WHERE user_id = %s ''' % (points, int(member.id)))
                # Adds lifetime points to the database
                await client.pool.execute(
                    '''UPDATE users SET lifetime = lifetime+%s WHERE user_id = %s ''' % (points, int(member.id)))

        # Wipes user's timestamp
        await client.pool.execute('''UPDATE users SET voice_join_timestamp = NULL WHERE user_id = %s''' % (member.id))


@client.event
async def on_ready():
    print('Bot is ready')
    guild_list = []

    channel = client.get_channel(601539314874187776)
    await channel.send('Bot is online')

    # Add all guilds to the guild list
    for guild in list(client.guilds):
        guild_list.append(guild.name)
        await client.pool.execute('''INSERT INTO guilds(guild_id, prefix) VALUES(%s, $$%s$$) ON CONFLICT DO NOTHING''' % (int(guild.id), '.'))

    # Wipes all timestamps to prevent bugs when bot crashes
    await client.pool.execute('''ALTER TABLE users DROP COLUMN voice_join_timestamp CASCADE''')
    await client.pool.execute('''ALTER TABLE users ADD COLUMN IF NOT EXISTS voice_join_timestamp TIMESTAMP''')

asyncio.get_event_loop().run_until_complete(create_db_pool())

# Bot token
client.run(token)
