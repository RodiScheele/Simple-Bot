import os

# The bot token can be configured as an environment variable or hardcoded (If you give no shit about security).
if os.getenv('DISCORD_TOKEN') != 0:
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    TOKEN = ""
PREFIX = "!"
DESCRIPTION = "I am a humble bot."
APPLICATION_ID = "833460245455044618"
if os.name == 'nt':
    DB_STRING = "mongodb://host.docker.internal:27017/"
else:
    DB_STRING = "mongodb://127.0.0.1:27017/"
DB_NAME = "simplebot"
# DB collections
DB_COLLECTION_DAILY_ROLL_VALUE = "dailyroll_value"
DB_COLLECTION_DAILY_ROLL_HISTORY = "dailyroll_roll_history"
DB_COLLECTION_DAILY_ROLL_SCORE = "dailyroll_score"
