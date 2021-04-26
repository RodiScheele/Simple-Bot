from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self._last_member = None

    @commands.command(name='ping')
    async def ping(self, context):
        await context.send('Pong!')


def setup(bot):
    bot.add_cog(Ping(bot))