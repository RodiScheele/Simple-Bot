import os
import sys
import discord
from discord.ext import commands
import logging
import command_handler

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load the Discord bot token from environment
if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    sys.exit("No environment token found, please configure this first.")

# Set up the bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', description='Bot', intents=intents)


# Code to run once the bot is logged in and ready
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    command_handler.load(client)


client.run(TOKEN)
