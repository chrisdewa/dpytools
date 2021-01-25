from discord.ext import commands
from typing import Union
from discord.utils import get

from dpytools.errors import Unauthorized, IncorrectGuild


def admin_or_roles(*role_ids: Union[int, str]) -> commands.check:
    """
    This check returns true under these conditions:
        The command is run in a guild AND:
            ctx.author has admin permissions OR
            has any role in :roles:

    Raises:
        commands.NoPrivateMessage if ran from DM
        Unauthorized if user doesn't have correct roles or admin permissions
        ValueError if value passed on role_ids is not int or str
    """

    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        if ctx.author.guild_permissions.administrator is True:
            return True

        roles = []
        for role in role_ids:
            if isinstance(role, str):
                roles.append(get(ctx.guild.roles, name=role))
            elif isinstance(role, int):
                roles.append(ctx.guild.get_role(role))
            else:
                raise ValueError(f"int or str was expected but received {type(role)}")
        if any([role for role in roles if role and role in ctx.author.roles]):
            return True
        else:
            raise Unauthorized("User doesn't have admin permissions or specified roles")

    return commands.check(predicate)


def only_this_guild(guild_id: int) -> commands.check:
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
