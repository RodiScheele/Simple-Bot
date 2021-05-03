from discord.ext import commands
from random import *
from datetime import datetime
import pymongo
from ..files import config
from ..database import roll_db


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.client = pymongo.MongoClient(config.DB_STRING)
        #self.database = config.DB_NAME
        #self.value_collection = config.DB_COLLECTION_ROLL_VALUE

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
            if value == 0:
                output_text = "Congrats!"
            else:
                output_text = "Sad :("
            await context.send(output_text)

    @commands.command(name='setdailyroll', description="Set the value for the daily roll.")
    async def set_daily_roll(self, context, arg1):
        """Set the value for the daily roll competition"""
        if not context.author.bot:
            output_text = None
            if await is_int(arg1):
                if 0 < int(arg1) <= 100:
                    roll_db.create_or_update_roll_value(context.guild.id, int(arg1), datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'), context.author.id)
                    output_text = "I've set the daily roll value to " + arg1 + ". Time to roll!"
                else:
                    output_text = "You must insert a value between 1 and 100."
            else:
                output_text = "I don't understand what you are trying to do. Try setting a value with !setdailyroll [number]"
            await context.send(output_text)

    @commands.command(name='getdailyroll', description="Get the value for the daily roll.")
    async def get_daily_roll(self, context):
        """Get the value for the daily roll competition."""
        if not context.author.bot:
            value = roll_db.get_roll_value(context.guild.id)
            if value is not None:
                output_text = "The current value has been set by <@" + str(value['user']) + "> and is: " + str(value['value']) + ". Try to roll this number with !dailyroll"
            else:
                output_text = "Daily roll value has not been set yet. Use !setdailyroll [number] to set a value first."
            await context.send(output_text)


async def is_int(parameter):
    value = True
    try:
        int(parameter)
    except ValueError:
        value = False

    return value


def setup(bot):
    bot.add_cog(Roll(bot))
