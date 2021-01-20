from discord.ext import commands

class IncorrectGuild(commands.CommandError):
    pass


def only_this_guild(guild_id: int):
    """This checks returns true if ctx.guild has same id as param :guild_id:
    Raises:
        commands.NoPrivateMessage if ran from DM
        Custom IncorrectGuild commands.CommandError if id doesn't check
    Returns:
        True if guild_id == ctx.guild.id
    """
    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        elif guild_id != ctx.guild.id:
            raise IncorrectGuild()
        return True

    return commands.check(predicate)