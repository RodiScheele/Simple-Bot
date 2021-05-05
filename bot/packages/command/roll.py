from discord.ext import commands
from random import *
from datetime import date
from ..database import roll_db
from operator import itemgetter


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            if roll_db.get_roll_value(context.guild.id) is not None:
                roll_goal = roll_db.get_roll_value(context.guild.id)['value']
                dte = date.today().strftime('%Y-%m-%d')
                roll_history = roll_db.get_roll_history(context.guild.id, dte)
                not_rolled = True
                prev_value = None
                for user in roll_history:
                    if int(user['user_id']) == context.author.id:
                        not_rolled = False
                        prev_value = user['value']
                        break

                if not_rolled:
                    value = randint(1, 100)
                    roll_db.add_roll_history(context.guild.id, dte, context.author.id, value)
                    if value == roll_goal:
                        score = await add_point(context)
                        point_str = "points"
                        if score == 1:
                            point_str = "point"

                        output_text = "You rolled " + str(
                            value) + ". Holy shit, you actually did it, you absolute madman! It's time for a party " \
                                     "@everyone, <@" + str(context.author.id) + "> is paying! Your score is now " \
                                     + str(score) + point_str + "."
                    else:
                        output_text = "You rolled " + str(value) + ". The goal was to roll " + str(
                            roll_goal) + ', better luck tomorrow.'
                elif not not_rolled:
                    output_text = "You have already rolled " + str(prev_value) + " today, try again tomorrow!"
            else:
                output_text = "Daily roll value has not been set yet. Use !setdailyroll [number] to set a value first."
            await context.send(output_text)

    @commands.command(name='setdailyroll', description="Set the value for the daily roll.")
    async def set_daily_roll(self, context, arg1):
        """Set the value for the daily roll competition"""
        if not context.author.bot:
            output_text = None
            if await is_int(arg1):
                if 0 < int(arg1) <= 100:
                    roll_db.create_or_update_roll_value(context.guild.id, int(arg1), date.today().strftime('%Y-%m-%d'),
                                                        context.author.id)
                    output_text = "I've set the daily roll value to " + arg1 + ". Time to roll!"
                else:
                    output_text = "You must insert a value between 1 and 100."
            else:
                output_text = "I don't understand what you are trying to do. Try setting a value with !setdailyroll [" \
                              "number] "
            await context.send(output_text)

    @commands.command(name='getdailyroll', description="Get the value for the daily roll.")
    async def get_daily_roll(self, context):
        """Get the value for the daily roll competition."""
        if not context.author.bot:
            value = roll_db.get_roll_value(context.guild.id)
            if value is not None:
                output_text = "The current value has been set by <@" + str(value['user_id']) + "> and is: " + str(
                    value['value']) + ". Try to roll this number with !dailyroll"
            else:
                output_text = "Daily roll value has not been set yet. Use !setdailyroll [number] to set a value first."
            await context.send(output_text)

    @commands.command(name='dailyrollscore', description="See the current highscores for !dailyroll.")
    async def get_daily_roll_score(self, context):
        """See the current highscores for !dailyroll."""
        if not context.author.bot:
            user_scores = roll_db.get_server_score(context.guild.id)
            user_scores_sorted = sorted(user_scores, key=itemgetter('score'), reverse=True)
            await context.send("High scores:")
            for user in user_scores_sorted:
                point_str = " points"
                if user['score'] == 1:
                    point_str = " point"
                await context.send(str(user['score']) + point_str + " - " + str(user['user_name']))
            await context.send("End of my list.")


async def is_int(parameter):
    value = True
    try:
        int(parameter)
    except ValueError:
        value = False

    return value


async def add_point(context):
    user_score = roll_db.get_user_score(context.guild.id, context.author.id)
    score = None
    if user_score is not None:
        score = int(user_score['score']) + 1
    else:
        score = 1
    roll_db.create_or_update_score(context.guild.id, context.author.id, score, context.author.nick)
    return score


def setup(bot):
    bot.add_cog(Roll(bot))
