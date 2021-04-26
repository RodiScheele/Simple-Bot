import os
import sys

if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    sys.exit("No DISCORD_TOKEN found in the environment variables, please configure DISCORD_TOKEN first.")
PREFIX = "!"
DESCRIPTION = "I am a humble bot."

