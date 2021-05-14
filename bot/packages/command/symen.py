from discord.ext import commands


class Symen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Borrowed from this author: https://github.com/bverpaalen/discord_ping_bot/blob/main/commands/everyone.py
    @commands.command(name='symen', description='What is even the point of this command?')
    async def symen(self, context, *args):
        """Deprecated command, use !ping instead."""
        if not context.author.bot:
            await context.message.channel.send("This command has been deprecated. Try using !ping [username] [amount]")
            """symen_strings = { 'symen', 'dogger', 'pyromancio'}
            match = False
            output_text = None
            for member in context.message.guild.members:
                if member.name.lower() in symen_strings or member.display_name.lower() in symen_strings:
                    match = True
                    output_text = "<@" + str(member.id) + ">!"
                    break
            if not match:
                output_text = "I could not find Symen here :("

            if len(args) == 0 or not match:
                await context.message.channel.send(output_text)
            elif len(args) == 1:
                if is_int(args[0]):
                    for i in range(0, int(args[0])):
                        if i < 10:
                            await context.message.channel.send(output_text)
                        if i >= 10:
                            await context.message.channel.send("I think that I have pinged " + output_text + " enough for now.")
                            break
                else:
                    await context.message.channel.send("What are you trying to do?")
            elif len(args) >= 2:
                await context.message.channel.send("What are you trying to do?")"""


def setup(bot):
    bot.add_cog(Symen(bot))