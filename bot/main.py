import discord
from discord.ext import commands
import logging
import os
from bot.packages.files import config
import packages.files
import packages.command

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


# Load all commands function
def load(bot):
    for file in os.listdir('packages/command/'):
        if file.endswith('.py') and not file.endswith('__init__.py'):
            try:
                bot.load_extension(f'packages.command.{file[:-3]}')
            except (Exception, ArithmeticError) as e:
                print("Could not load " + file)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                print(template.format(type(e).__name__, e.args))


# Code to run once the bot is logged in and ready
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    # Load the command_handler once the bot runs
    load(client)


# Start the bot
client.run(config.TOKEN)
