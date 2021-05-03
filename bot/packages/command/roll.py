from discord.ext import commands
from random import *
from datetime import date
import pymongo
from ..files import config


class Roll(commands.Cog):
    def __init__(self, bot, daily_roll_val=0):
        self.bot = bot
        self.daily_roll_val = daily_roll_val
        self.daily_roll_date = date.today()
        self.daily_roll_user = None

    @commands.command(name='roll', description="Roll a dice. The default dice is set between 1 and 100, you can "
                                               "provide arguments to alter the dice with '!roll [maximum_value]' or "
                                               "'!roll [minimum_value] [maximum_value]'")
    async def roll(self, context, *args):
        """Roll a dice"""
        if not context.author.bot:
            output_text = None

            if len(args) == 0:
                value = randint(1, 100)
                output_text = "Rolling between 1 and 100!\n" + str(value)
            elif len(args) == 1:
                if await is_int(args[0]):
                    value = randint(1, int(args[0]))
                    output_text = "Rolled between 1 and " + args[0] + "!\n" + str(value)
                else:
                    output_text = "I require a whole number!"
            elif len(args) == 2:
                if await is_int(args[0]) and await is_int(args[1]):
                    if int(args[0]) >= int(args[1]):
                        output_text = "The first number can't be larger or equal than the second number!"
                    else:
                        value = randint(int(args[0]), int(args[1]))
                        output_text = "Rolled between " + args[0] + " and " + args[1] + "!\n" + str(value)
                else:
                    output_text = "I require whole numbers!"
            elif len(args) > 2:
                output_text = "I only take a maximum of two arguments!"

            await context.send(output_text)

    @commands.command(name='dailyroll', description="Roll a dice between 1 and 100 and try to win the daily roll!")
    async def daily_roll(self, context):
        """Daily roll competition"""
        if not context.author.bot:
            output_text = None

            value = randint(1, 100)
            if value == self.daily_roll_val:
                output_text = "Congrats!"
            else:
                output_text = "Sad :("

    @commands.command(name='setdailyroll', description="Set the value for the daily roll.")
    async def set_daily_roll(self, context, arg1):
        """Set the value for the daily roll competition"""
        if not context.author.bot:
            output_text = None
            if is_int(arg1):
                output_text = "yes"
            else:
                output_text = "no"

    @commands.command(name='getdailyroll', description="Get the value for the daily roll.")
    async def get_daily_roll(self, context):
        """Get the value for the daily roll competition."""
        if not context.author.bot:
            output_text = "The current goal is to roll " + str(self.daily_roll_val) + "."

            myclient = pymongo.MongoClient(config.DB_STRING)

            mndb = myclient["simplebot"]
            print(mndb.list_collection_names())
            await context.send(output_text)


async def is_int(parameter):
    value = True
    try:
        int(parameter)
    except ValueError:
        value = False

    return value


async def check_user(user):

    return None

def setup(bot):
    bot.add_cog(Roll(bot))
