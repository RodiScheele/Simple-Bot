from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, context):
        await context.send('Pong!')

    @commands.command(name='pong')
    async def pong(self, context):
        await context.send('Ping!')


def setup(bot):
    bot.add_cog(Ping(bot))