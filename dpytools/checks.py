from discord.ext import commands
from typing import Union
from discord.utils import get


class IncorrectGuild(commands.CommandError):
    pass


class Unauthorized(commands.CommandError):
    pass


def admin_or_roles(*roles: Union[int, str]) -> bool:
    """
    This check returns true under these conditions:
        The command is run in a guild AND:
            ctx.author has admin permissions OR
            has any role in :roles:

    Raises:
        commands.NoPrivateMessage if ran from DM
        Unauthorized if user doesn't have correct roles or admin permissions
    """

    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        role_objs = []
        for role in roles:
            if isinstance(role, str):
                role_objs.append(get(ctx.guild.roles, name=role))
            elif isinstance(role, int):
                role_objs.append(ctx.guild.get_role(role))
            else:
                raise ValueError(f"Int or Str was expected but received {type(role)}")
        if any([role for role in role_objs if role and role in ctx.author.roles]):
            return True
        else:
            raise Unauthorized("User doesn't have admin permissions or specified roles")

    return commands.check(predicate)


def only_this_guild(guild_id: int) -> bool:
    """This check returns true if ctx.guild has same id as param :guild_id:

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
