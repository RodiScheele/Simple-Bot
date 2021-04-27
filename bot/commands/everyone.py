from discord.ext import commands


class Everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='everyone', description='Pings everyone by their name, alternative to @everyone')
    async def everyone(self, context):
        """Pings everyone by their name"""
        member_list = "PING PING PING "
        for member in context.message.guild.members:
            if member.id != self.bot.user.id:
                member_list += "<@" + str(member.id) + "> "
        await context.message.channel.send(member_list)


def setup(bot):
    bot.add_cog(Everyone(bot))
