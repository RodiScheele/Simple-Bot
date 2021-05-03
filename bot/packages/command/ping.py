from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='ping', description='Ping! :)')
    async def ping(self, context):
        """Do a ping!"""
        if not context.author.bot:
            member = context.author
            if self._last_member is not None:
                await context.send("Pong! Back to <@" + str(self._last_member.id) + ">.")
            else:
                await context.send("Pong!")
            self._last_member = member

    @commands.command(name='pong', description='Pong! (:')
    async def pong(self, context):
        """Do a pong!"""
        if not context.author.bot:
            member = context.author
            if self._last_member is not None:
                await context.send("Ping! Back to <@" + str(self._last_member.id) + ">.")
            else:
                await context.send("Ping!")
            self._last_member = member


def setup(bot):
    bot.add_cog(Ping(bot))