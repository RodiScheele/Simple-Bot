import os
import sys
import discord
from discord.ext import commands as cd
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    sys.exit('No environment token found, please configure this first.')

intents = discord.Intents.default()
intents.members = True
client = cd.Bot(command_prefix='!', description='Bot', intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

client.run(TOKEN)
