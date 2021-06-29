from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def everyone(self, context):
        """Pings everyone by their name"""
        if not context.author.bot:
            member_list = "PING PING PING "
            for member in context.channel.members:
                if member.id and not member.bot:
                    member_list += "<@" + str(member.id) + "> "
            await context.channel.send(member_list)

    @commands.command(name="everyone", description='Pings everyone by their name, alternative to @everyone')
    async def everyone_command(self, context):
        await self.everyone(context)

    @cog_ext.cog_slash(name="everyone", description='Pings everyone by their name, alternative to @everyone')
    async def everyone_slash(self, context: SlashContext):
        await self.everyone(context)


def setup(bot):
    bot.add_cog(Everyone(bot))
