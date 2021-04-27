from discord.ext import commands
import random

class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='insult', description="Insults you or someone else with '!insult [optional:name]'")
    async def insult(self, context, *args):
        """Insults you or someone else"""
        insult = get_insult()
        output_text = None
        if len(args) == 0 or len(args) > 1:
            output_text = "<@" + str(context.author.id) + "> " + insult
        else:
            match = False
            for member in context.message.guild.members:
                if args[0].lower() == member.name.lower() or args[0].lower() == member.display_name.lower():
                    match = True
                    output_text = "<@" + str(member.id) + "> " + insult
                    break
            if not match:
                output_text = "I could not find the person you are trying to insult."

        await context.send(output_text)


# TODO: Optimize for memory.
def get_insult():
    lines = open('./files/insult_list.txt').read().splitlines()
    line = random.choice(lines)
    return line


def setup(bot):
    bot.add_cog(Insult(bot))