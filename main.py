import discord
import os
from discord.ext import commands
import asyncio
import asyncpg
import logging


# Connects to database
async def create_db_pool():
    pool = await asyncpg.create_pool(host='127.0.0.1', database='GameBot', user='postgres', password='admin123')
    con = await pool.acquire()

# Logs to console
logging.basicConfig(level=logging.INFO)

client = discord.Client()
token = 'MjcyMjYwMDYyNzkyMTIyMzY4.XS9O1Q.fl1ghrEgvrLP0svKo-k5wX3lmd0'


@client.event
async def on_ready():
    print('Bot is ready')

# Athena token
client.run(token)
asyncio.get_event_loop().run_until_complete(create_db_pool())