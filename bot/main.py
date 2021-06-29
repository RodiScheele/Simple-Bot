import discord
from discord.ext import commands
from discord_slash import SlashCommand
import logging
import os
from packages.files import config


# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up the bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config.PREFIX, description=config.DESCRIPTION, intents=intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


# Load all commands
def load_commands():
    for file in os.listdir('packages/command/'):
        if file.endswith('.py') and not file.endswith('__init__.py'):
            try:
                bot.load_extension(f'packages.command.{file[:-3]}')
            except (Exception, ArithmeticError) as e:
                print("Could not load " + file)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                print(template.format(type(e).__name__, e.args))


# Code to run once the bot is logged in and ready
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name='!help | Pretty sus'))


# Start the bot
load_commands()
bot.run(config.TOKEN)
