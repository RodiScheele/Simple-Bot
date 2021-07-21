from discord.ext import commands
from random import *
from datetime import date
from ..database import roll_db
from ..logic import functions
from operator import itemgetter
from discord_slash import cog_ext, SlashContext


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def roll(self, context, *args):
        if not context.author.bot:
            output_text = None

            if len(args) == 0:
                value = randint(1, 100)
                output_text = "Rolling between 1 and 100!\n" + str(value)
            elif len(args) == 1:
                if await functions.is_int(args[0]):
                    value = randint(1, int(args[0]))
                    output_text = "Rolled between 1 and " + args[0] + "!\n" + str(value)
                else:
                    output_text = "I require a whole number!"
            elif len(args) == 2:
                if await functions.is_int(args[0]) and await functions.is_int(args[1]):
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

    @commands.command(name='roll', description="Roll a dice. The default dice is set between 1 and 100, you can "
                                               "provide arguments to alter the dice with '!roll [maximum_value]' or "
                                               "'!roll [minimum_value] [maximum_value]'")
    async def roll_command(self, context, *args):
        """Roll a dice"""
        await self.roll(context, *args)

    @cog_ext.cog_slash(name='roll', description="Roll a dice with '/roll [minimum_value] [maximum_value]' or '!roll")
    async def roll_slash(self, context: SlashContext, arg1, arg2):
        """Roll a dice"""
        args = (arg1, arg2)
        await self.roll(context, *args)

    async def daily_roll(self, context):
        if not context.author.bot:
            output_text = None
            if roll_db.get_roll_value(context.guild.id) is not None:
                roll_goal = roll_db.get_roll_value(context.guild.id)['value']
                dte = date.today().strftime('%Y-%m-%d')
                roll_history = roll_db.get_roll_history_date(context.guild.id, dte)
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
                                     + str(score) + " " + point_str + "."
                    else:
                        output_text = "You rolled " + str(value) + ". The goal was to roll " + str(
                            roll_goal) + ', better luck tomorrow.'
                elif not not_rolled:
                    output_text = "You have already rolled " + str(prev_value) + " today, try again tomorrow!"
            else:
                output_text = "Daily roll value has not been set yet. Use !setdailyroll [number] to set a value first."
            await context.send(output_text)

    @commands.command(name='dailyroll', description="Roll a dice between 1 and 100 and try to win the daily roll!")
    async def dailyroll_command(self, context):
        """Compete in the daily roll!"""
        await self.daily_roll(context)

    @cog_ext.cog_slash(name='dailyroll', description="Roll a dice between 1 and 100 and try to win the daily roll!")
    async def dailyroll_slash(self, context: SlashContext):
        """Compete in the daily roll!"""
        await self.daily_roll(context)

    async def set_daily_roll(self, context, arg1):
        if not context.author.bot:
            output_text = None
            if await functions.is_int(arg1):
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

    @commands.command(name='setdailyroll', description="Set the value for the daily roll.")
    async def set_daily_roll_command(self, context, arg1):
        """Set a value for the daily roll competition."""
        await self.set_daily_roll(context, arg1)

    @cog_ext.cog_slash(name='setdailyroll', description="Set the value for the daily roll.")
    async def set_daily_roll_slash(self, context: SlashContext, arg1):
        """Set a value for the daily roll competition."""
        await self.set_daily_roll(context, arg1)

    async def get_daily_roll(self, context):
        if not context.author.bot:
            value = roll_db.get_roll_value(context.guild.id)
            if value is not None:
                output_text = "The current value has been set by <@" + str(value['user_id']) + "> and is: " + str(
                    value['value']) + ". Try to roll this number with !dailyroll"
            else:
                output_text = "Daily roll value has not been set yet. Use !setdailyroll [number] to set a value first."
            await context.send(output_text)

    @commands.command(name='getdailyroll', description="Get the value for the daily roll.")
    async def get_daily_roll_command(self, context):
        """Get the value for the daily roll competition."""
        await self.get_daily_roll(context)

    @cog_ext.cog_slash(name='getdailyroll', description="Get the value for the daily roll.")
    async def get_daily_roll_slash(self, context: SlashContext):
        """Get the value for the daily roll competition."""
        await self.get_daily_roll(context)

    async def get_daily_roll_score(self, context):
        if not context.author.bot:
            user_scores = roll_db.get_server_score(context.guild.id)
            user_scores_sorted = sorted(user_scores, key=itemgetter('score'), reverse=True)

            output_str = "```High Scores:\n"
            for user in user_scores_sorted:
                point_str = " points"
                if user['score'] == 1:
                    point_str = " point"
                output_str += str(user['score']) + point_str + " - " + str(user['user_name']) + "\n"
            output_str += "```"

            await context.send(output_str)

    @commands.command(name='dailyrollscore', description="See the current scores for !dailyroll.")
    async def get_daily_roll_score_command(self, context):
        """See the current highscores for dailyroll."""
        await self.get_daily_roll_score(context)

    @cog_ext.cog_slash(name='dailyrollscore', description="See the current scores for dailyroll.")
    async def get_daily_roll_score_slash(self, context: SlashContext):
        """See the current highscores for dailyroll."""
        await self.get_daily_roll_score(context)

    async def daily_roll_statistics(self, context):
        if not context.author.bot:
            rolls = roll_db.get_roll_history_all(context.guild.id)
            total_rolls = rolls.count()
            user_rolls = roll_db.get_roll_history_user(context.guild.id, context.author.id)
            total_user_rolls = user_rolls.count()

            roll_list = []
            for roll in rolls:
                roll_list.append(roll['value'])

            if len(roll_list) != 0:
                most_rolled_val = max(set(roll_list), key=roll_list.count)
                most_rolled_val_count = roll_list.count(most_rolled_val)
                target_roll_value = roll_db.get_roll_value(context.guild.id)['value']
                target_rolls = roll_list.count(target_roll_value)
            else:
                most_rolled_val = 0
                most_rolled_val_count = 0
                target_roll_value = 0
                target_rolls = 0

            output_str = "```Dailyroll statistics.\n" \
                         "Total rolls done on server: " + str(total_rolls) + "\n" \
                         "Total rolls done by you: " + str(total_user_rolls) + "\n" \
                         "Total rolls done on server for current target (" + str(target_roll_value) + "): " + str(target_rolls) + "\n" \
                         "The most rolled value is " + str(most_rolled_val) + " which has been rolled a staggering " + str(most_rolled_val_count) + " times!" \
                         "```"
            await context.send(output_str)

    @commands.command(name='dailyrollstats', description="View the server stats for dailyroll")
    async def daily_roll_statistics_command(self, context):
        """See the server stats for !dailyroll"""
        await self.daily_roll_statistics(context)

    @cog_ext.cog_slash(name='dailyrollstats', description="View the server stats for dailyroll")
    async def daily_roll_statistics_slash(self, context: SlashContext):
        """See the server stats for !dailyroll"""
        await self.daily_roll_statistics(context)

    async def daily_roll_breakdown(self, context):
        if not context.author.bot:
            rolls = roll_db.get_roll_history_all(context.guild.id)

            roll_list = []
            for roll in rolls:
                roll_list.append(roll['value'])

            roll_dict = dict()
            for roll in roll_list:
                if roll in roll_dict:
                    roll_dict[roll] += 1
                else:
                    roll_dict[roll] = 1

            output_str = "```"
            for key, value in roll_dict.items():
                output_str = output_str + str(key) + " : " + str(value) + "\n"
            output_str = output_str + "```"
            await context.send(output_str)

    @commands.command(name='dailyrollbreakdown', description="View the server breakdown for dailyroll")
    async def daily_roll_breakdown_command(self, context):
        """View the server breakdown for !dailyroll"""
        await self.daily_roll_breakdown(context)

    @cog_ext.cog_slash(name='dailyrollbreakdown', description="View the server breakdown for dailyroll")
    async def daily_roll_breakdown_slash(self, context: SlashContext):
        """View the server breakdown for !dailyroll"""
        await self.daily_roll_breakdown(context)


async def add_point(context):
    user_score = roll_db.get_user_score(context.guild.id, context.author.id)
    score = None
    if user_score is not None:
        score = int(user_score['score']) + 1
    else:
        score = 1
    name = context.author.nick
    if name is None:
        name = context.author.name
    roll_db.create_or_update_score(context.guild.id, context.author.id, score, name)
    return score


def setup(bot):
    bot.add_cog(Roll(bot))
