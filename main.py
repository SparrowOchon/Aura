import discord
import os
from discord.ext import commands
import asyncio
import asyncpg
import logging
import datetime


# Logs to console
logging.basicConfig(level=logging.INFO)

token = 'MjcyMjYwMDYyNzkyMTIyMzY4.XS9O1Q.fl1ghrEgvrLP0svKo-k5wX3lmd0'
client = commands.Bot(command_prefix='.')

# Loop to look through cogs folder and load all cogs contained within it
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # splicing cuts 3 last characters aka .py
        client.load_extension(f'cogs.{filename[:-3]}')


# Connects to database
async def create_db_pool():
    client.pool = await asyncpg.create_pool(host='127.0.0.1', database='GameBot', user='postgres', password='admin123')

    # Creates the user database
    await client.pool.execute('''CREATE TABLE IF NOT EXISTS users( 
                        user_id BIGINT,
                        text_messages INTEGER,
                        voice_time INTEGER,
                        points DECIMAL,
                        voice_join_timestamp VARCHAR[30],
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
                            PRIMARY KEY(guild_id))''')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    member = message.author

    # Add users into the database if they're not there
    await client.pool.execute('''INSERT INTO users(user_id, text_messages, voice_time, points, voice_join_timestamp) VALUES(%s, %s, %s, %s, NULL) ON CONFLICT DO NOTHING''' % (int(member.id), int(0), int(0), int(0)))

    # Adds the text message to the database
    await client.pool.execute('''UPDATE users SET text_messages = text_messages+1 WHERE user_id = %s ''' % (int(member.id)))

    print(f'{message.author} in {message.author.guild.name}: {message.content}')
    await client.process_commands(message)


@client.event
async def on_voice_state_update(member, before, after):

    # User joined the channel
    if before.channel is None and after.channel is not None:
        print(member, 'joined ', after.channel, ' in ', member.guild.name)

        # Adds user to the database if they are not in it
        await client.pool.execute(
            '''INSERT INTO users(user_id, text_messages, voice_time, points) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING''' % (int(member.id), int(0), int(0), int(0)))

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

        # Wipes user's timestamp
        await client.pool.execute('''UPDATE users SET voice_join_timestamp = NULL WHERE user_id = %s''' % (member.id))


@client.event
async def on_ready():
    print('Bot is ready')
    guild_list = []

    # Add all guilds to the guild list
    for guild in list(client.guilds):
        guild_list.append(guild.name)
        await client.pool.execute('''INSERT INTO guilds(guild_id) VALUES(%s) ON CONFLICT DO NOTHING'''% (int(guild.id)))

    # Wipes all timestamps to prevent bugs when bot crashes
    await client.pool.execute('''ALTER TABLE users DROP COLUMN voice_join_timestamp CASCADE''')
    await client.pool.execute('''ALTER TABLE users ADD COLUMN IF NOT EXISTS voice_join_timestamp TIMESTAMP''')

asyncio.get_event_loop().run_until_complete(create_db_pool())

# Bot token
client.run(token)
