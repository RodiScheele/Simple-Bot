from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}. I sure hope that you are not some kind of imposter?'.format(member))

    async def hello(self, context):
        """Says hello"""
        if not context.author.bot:
            member = context.author
            if self._last_member is None or self._last_member.id != member.id:
                await context.send('Hello {0.name}~'.format(member))
            else:
                await context.send('Hello {0.name}... This feels familiar.'.format(member))
            self._last_member = member

    @commands.command(name="hello", description='Says hello!')
    async def hello_command(self, context):
        await self.hello(context)

    @cog_ext.cog_slash(name="hello", description='Says hello!')
    async def hello_slash(self, context):
        await self.hello(context)


def setup(bot):
    bot.add_cog(Greetings(bot))
