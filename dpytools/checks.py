# -*- coding: utf-8 -*-
"""
This module holds different command checks to add as decorator for custom commands.
Use this checks on your code like this:
    ```
    @bot.command()
    @admin_or_roles('Moderator')
    async def mute(ctx, member: discord.Member):
        ...
    ```
Or inside Cogs:
    ```
    @commands.command()
    @only_this_guild(123456789...)
    async def magic(self, ctx):
        ...
    ```

"""


from discord.ext import commands
from discord.ext.commands import PrivateMessageOnly
from typing import Union, List
from discord.utils import get

from dpytools.errors import Unauthorized, IncorrectGuild, NotMemberOfCorrectGuild


def admin_or_roles(*roles: Union[int, str]) -> commands.check:
    """
    This check returns true under these conditions:
        The command is run in a guild AND:
            ctx.author has admin permissions OR has any role in :roles:

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

        discord_roles = []
        for role in roles:
            if isinstance(role, str):
                discord_roles.append(get(ctx.guild.roles, name=role))
            elif isinstance(role, int):
                discord_roles.append(ctx.guild.get_role(role))
            else:
                raise ValueError(f"int or str was expected but received {type(role)}")
        if any([role for role in discord_roles if role in ctx.author.roles]):
            return True
        else:
            raise Unauthorized("User doesn't have admin permissions or specified roles")

    return commands.check(predicate)


def only_this_guild(guild_id: int) -> commands.check:
    """This check returns true if ctx.guild has same id as param :guild_id:

    Raises:
        commands.NoPrivateMessage if ran from DM
        Custom IncorrectGuild commands.CommandError if id doesn't check

    """

    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage("Command was called from a direct message.")
        elif guild_id != ctx.guild.id:
            raise IncorrectGuild(f"Command was called from a guild with id different than specified in check")
        return True

    return commands.check(predicate)


def dm_from_this_guild(guild_id: int, delete: bool = False) -> commands.check:
    """
    The check returns true only if the specified :guild_id: is found within the bot's guilds.
    For this check to work the guilds and members intents must be enabled.

    Args:
        guild_id: id of the guild the author of the context must be a part of for check to return True
        delete: if True, it will try to delete ctx.message. This will only happen if the message is called
                from the specificed guild_id, if the command is called from another guild the check will
                just return False.

            Possible exceptions by discord.py library:
                commands.Forbidden – You do not have proper permissions to delete the message.
                commands.NotFound – The message was deleted already
                commands.HTTPException – Deleting the message failed.

    Returns:
        commands.check

    Raises:
        commands.PrivateMessageOnly: if called from a guild
        dpytools.errors.NotMemberOfCorrectGuild: if not a member of the specified guild
    """
    async def predicate(ctx):
        if ctx.guild and ctx.guild.id == guild_id:
            if delete is True:
                await ctx.message.delete()
            raise PrivateMessageOnly("Command was called from the guild instead of a direct message.")
        elif ctx.guild:
            return False

        guild = ctx.bot.get_guild(guild_id)

        if ctx.author in guild.members:
            return True
        else:
            raise NotMemberOfCorrectGuild("This command is unavailable to you.")

    return commands.check(predicate)

