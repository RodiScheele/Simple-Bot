from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', description='Ping! :)')
    async def ping(self, context):
        """Do a ping!"""
        await context.send('Pong!')

    @commands.command(name='pong', description='Ping! (:')
    async def pong(self, context):
        """Do a pong!"""
        await context.send('Ping!')


def setup(bot):
    bot.add_cog(Ping(bot))