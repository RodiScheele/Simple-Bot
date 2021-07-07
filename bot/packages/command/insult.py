from discord.ext import commands
import random
from pathlib import Path
from discord_slash import cog_ext, SlashContext


class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def insult(self, context, arg):
        """Insults you or someone else"""
        if not context.author.bot:
            insult_str = get_insult()
            output_text = None

            match = False
            for member in context.message.guild.members:
                if arg.lower() == member.name.lower() or arg.lower() == member.display_name.lower():
                    match = True
                    output_text = "<@" + str(member.id) + "> " + insult_str
                    break
            if not match:
                output_text = "I could not find the person you are trying to insult."

            await context.send(output_text)

    @commands.command(name="insult", description="Insults you or someone else with '!insult [optional:name]'")
    async def insult_command(self, context, arg):
        await self.insult(context, arg)

    @cog_ext.cog_slash(name="insult", description="Insults you or someone else with '!insult [optional:name]'")
    async def insult_slash(self, context: SlashContext, arg):
        await self.insult(context, arg)


# TODO: Optimize for memory, currently loads entire file every time when this command is called.
def get_insult():
    path = Path(__file__).parent / '../files/insult_list.txt'
    lines = open(path).read().splitlines()
    line = random.choice(lines)
    return line


def setup(bot):
    bot.add_cog(Insult(bot))