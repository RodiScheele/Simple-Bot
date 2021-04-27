from discord.ext import commands
from random import *


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', description="Roll a dice. The default dice is set between 1 and 100, you can "
                                               "provide arguments to alter the dice with '!roll [maximum_value]' or "
                                               "'!roll [minimum_value] [maximum_value]'")
    async def roll(self, context, *args):
        """Roll a dice"""
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


async def is_int(parameter):
    value = True
    try:
        int(parameter)
    except ValueError:
        value = False

    return value


def setup(bot):
    bot.add_cog(Roll(bot))
