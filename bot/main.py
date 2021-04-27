import os
import sys
import discord
from discord.ext import commands
import logging
import command_handler

# Load config file
if not os.path.isfile("files/config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    from bot.files import config

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up the bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=config.PREFIX, description=config.DESCRIPTION, intents=intents)


# Code to run once the bot is logged in and ready
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    # Load the command_handler once the bot runs
    command_handler.load(client)

# Start the bot
client.run(config.TOKEN)