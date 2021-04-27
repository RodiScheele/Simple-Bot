import os

# The bot token can be configured as an environment variable or hardcoded (If you give no shit about security).
if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    TOKEN = ""
PREFIX = "!"
DESCRIPTION = "I am a humble bot."
APPLICATION_ID = "833460245455044618"
