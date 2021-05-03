import os

# The bot token can be configured as an environment variable or hardcoded (If you give no shit about security).
if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    TOKEN = ""
PREFIX = "!"
DESCRIPTION = "I am a humble bot."
APPLICATION_ID = "833460245455044618"
DB_STRING = "mongodb://localhost:27017/"
DB_NAME = "simplebot"
DB_COLLECTION_DAILY_ROLL_VALUE = "dailyroll_value"
DB_COLLECTION_DAILY_ROLL_HISTORY = ""