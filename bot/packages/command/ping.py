from discord.ext import commands
from ..logic import functions
from discord_slash import cog_ext, SlashContext


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ping(self, context, *args):
        if not context.author.bot:
            # If 1 argument is given ping someone his username once
            if len(args) == 1:
                member = find_user(context, str(args[0]))
                if member is not None:
                    await context.send("Ping! " + "<@" + str(member) + ">!")
                else:
                    await context.send("I could not find that member.")
            # If 2 arguments are given ping someone his username multiple times (based on parameter)
            elif len(args) == 2:
                member = find_user(context, str(args[0]))
                if member is not None:
                    if await functions.is_int(args[1]):
                        for i in range (0, int(args[1])):
                            await context.send("PING PING PING " + "<@" + str(member) + ">!")
                            if i > 23:
                                await context.send("So much spam...")
                                break
                    else:
                        await context.send("You need to set a number. Try using ping [username] [amount]")
                else:
                    await context.send("I could not find that member. Try using ping [username] [amount]")
            # If none of the correct parameters are given do this.
            else:
                await context.send("Pong.")

    @commands.command(name="ping", description="Ping! :)")
    async def ping_command(self, context, *args):
        """Ping someone!"""
        await self.ping(context, *args)

    @cog_ext.cog_slash(name="ping", description="Ping! :)")
    async def ping_slash(self, context: SlashContext, arg1, arg2):
        """Ping someone!"""
        args = (arg1, arg2)
        await self.ping(context, *args)

    async def pong(self, context):
        if not context.author.bot:
            await context.send("Ping!")

    @commands.command(name='pong', description='Pong! (:')
    async def pong_command(self, context):
        """Do a pong!"""
        await self.pong(context)

    @cog_ext.cog_slash(name='pong', description='Pong! (:')
    async def pong_slash(self, context: SlashContext, *args):
        """Do a pong!"""
        await self.pong(context)


def find_user(context, username):
    for member in context.channel.members:
        if member.name.lower() == username.lower():
            return member.id
        if member.nick is not None:
            if member.nick.lower() == username.lower():
                return member.id
        if member.display_name is not None:
            if member.display_name.lower() == username.lower():
                return member.id
    return None


def setup(bot):
    bot.add_cog(Ping(bot))