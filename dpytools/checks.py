# -*- coding: utf-8 -*-
"""
Checks ready to use with **discord.ext.commands**
"""
from copy import copy
from datetime import datetime, time, timezone
from typing import Union

from discord import Member, Permissions
from discord import utils
from discord.ext import commands
from discord.ext.commands import PrivateMessageOnly, Context, MissingPermissions

from dpytools import _silent_except
from dpytools.errors import IncorrectGuild, NotMemberOfCorrectGuild, OutsidePermittedDatetime

__all__ = (
    'admin_or_roles',
    'only_this_guild',
    'dm_from_this_guild',
    'any_of_permissions',
    'this_or_higher_role',
    'between_times',
    'between_datetimes',
    'only_these_users',
    'in_these_channels',
    'is_guild_owner',
    'any_checks',
)


def admin_or_roles(*roles: Union[int, str]) -> commands.check:
    """
    Returns True under these conditions:

        - The command is run in a **guild**
        - **ctx.author** has admin permissions OR has any role in :param roles:

    Parameters
    ----------
    roles: :class:`Union[int,str]`
        Any number of strings or integers corresponding to the desired roles

    Raises
    ------
        :class:`discord.ext.commands.NoPrivateMessage`
            If ran from DM
        :class:`discord.ext.commands.MissingPermissions`
            If user doesn't have correct roles or admin permissions
    """

    async def predicate(ctx):

        if not all(type(r) in [int, str] for r in roles):
            raise TypeError('Roles must be type int or str')

        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        if ctx.author.guild_permissions.administrator is True:
            return True

        discord_roles = []
        for role in roles:
            if isinstance(role, str):
                discord_roles.append(utils.get(ctx.guild.roles, name=role))
            elif isinstance(role, int):
                discord_roles.append(ctx.guild.get_role(role))
            else:
                raise TypeError(f'int or str was expected but received "{type(role)}"')

        if not discord_roles:
            raise ValueError('No role in the server matched parameters')

        if any([role for role in discord_roles if role and role in ctx.author.roles]):
            return True
        else:
            raise commands.MissingPermissions("User doesn't have admin permissions or specified roles")

    return commands.check(predicate)


def only_this_guild(guild_id: int) -> commands.check:
    """
    Returns True under the following conditions:

        - **ctx.guild** has same id as :param guild_id:

    Raises
    ------
        :class:`discord.ext.commands.NoPrivateMessage`
            If ran outside a guild
        :class:`IncorrectGuild`
            If id doesn't check
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
    Returns True under the following conditions:

        - :param guild_id: is found within the **ctx.bot.guilds**.
        - **ctx.guild** is **None**

    For this check to work the guilds and members intents must be enabled.

    Parameters
    ----------
        guild_id: :class:`int`
            id of the guild the author of the context must be a part of
        delete: :class:`bool` (default: **False**)
                If True, it will try to delete ctx.message. This will only happen if the message is called
                from the specificed guild_id, if the command is called from another guild the check will
                just return False.

    Raises
    ------
        :class:`discord.ext.commands.PrivateMessageOnly`
            If called from a guild
        :class:`NotMemberOfCorrectGuild`
            If not a member of the specified guild
    """

    async def predicate(ctx):
        if ctx.guild and ctx.guild.id == guild_id:
            if delete is True:
                await ctx.message.delete()
            raise PrivateMessageOnly("Command was called from the guild instead of a direct message.")
        elif ctx.guild:
            return False

        guild = ctx.bot.get_guild(guild_id)
        if not guild:
            raise ValueError("Guild not found in the bot's guild cache")
        if ctx.author in guild.members:
            return True
        else:
            raise NotMemberOfCorrectGuild("This command is unavailable to you.")

    return commands.check(predicate)


def any_of_permissions(**permissions) -> commands.check:
    """
    Returns True under the following conditions:

        - **ctx.author** matches any permission passed in the decorator

    Parameters
    ----------
        permissions:
            appropriate permission flags. Keys are the permissions names and values the :class:`bool` setting

    Example
    -------
        The command below will send **success** only if **ctx.author** has any or more of **administrator**,
        **manage_guild** or **manage_messages** permissions::

            @bot.command()
            @any_of_permissions(administrator=True, manage_guild=True, manage_messages=True)
            async def test(ctx):
                await ctx.send('success')

    Raises
    ------
        :class:`discord.ext.commands.NoPrivateMessage`
            If ran outside a guild
        :class:`discord.ext.commands.MissingPermissions`
            If ctx.author does not have any of the passed permissions
    """

    async def predicate(ctx):
        if invalid := (set(permissions) - set(Permissions.VALID_FLAGS)):
            raise TypeError('Invalid permission(s): %s' % (', '.join(invalid)))
        elif ctx.guild is None:
            raise commands.NoPrivateMessage("Command was called from a direct message.")

        author: Member = ctx.author
        author_perms: Permissions = author.guild_permissions
        matched = [k for k, v in permissions.items() if getattr(author_perms, k) == v]
        if any(matched):
            return True
        else:
            raise commands.MissingPermissions("'You are missing one or more permission(s) to run this command.")

    return commands.check(predicate)


def this_or_higher_role(role: Union[str, int]) -> commands.check:
    """
    Returns True under the following conditions:
        - **ctx.author** has the specified role or another hierarchically higher

    Parameters
    ----------
        role: :class:`Union[str, int]`
            The role as its name (case sensitive) or id (int).

    Raise
    -----
        :class:`discord.ext.commands.NoPrivateMessage`
            If called outside a guild
    """

    def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command can only be used in a server.')
        author: Member = ctx.author

        if type(role) not in [int, str]:
            raise TypeError('Roles must be type int or str')

        drole = utils.get(ctx.guild.roles, name=role) if isinstance(role, str) else ctx.guild.get_role(role)

        if not drole:
            raise ValueError(f'No role found within guild {ctx.guild.name} with name or id "{role}"')

        return author.top_role >= drole

    return commands.check(predicate)


def between_times(from_time: time, to_time: time) -> commands.check:
    """
    Returns True under the following conditions:
        - **ctx.message.created_at.time()** is in the interval from :param from_time: to :param to_time:

    .. note::
        Parameters must be :class:`datetime.time` instances

    Parameters
    ----------
        from_time: :class:`datetime.time`
        to_time: :class:`datetime.time`
    """

    def predicate(ctx: Context):
        cmd_time = ctx.message.created_at.time()
        return from_time <= cmd_time <= to_time

    return commands.check(predicate)


def between_datetimes(from_dt: datetime,
                      to_dt: datetime,
                      ) -> commands.check:
    """
    Returns True under the following conditions:
        - **ctx.message.created_at** is in the interval from :param from_dt: to :param to_dt:

    .. note::
        Parameters must be of type :class:`datetime`

    .. note::
        If parameters are timezone aware they must share the same timezone.
        In this case The check will convert **ctx.message.created_at** to the timezone of the parameters

    Parameters
    ----------
        from_dt: :class:`datetime`
        to_dt: :class:`datetime`
    """

    def predicate(ctx: Context):
        tzs = (from_dt.tzinfo, to_dt.tzinfo)
        if any(tzs) and not all(tzs):
            raise TypeError("Either from_dt and to_dt must be both aware or both naive")

        dt: datetime = ctx.message.created_at

        if all(tzs):
            if tzs[0] != tzs[1]:
                raise ValueError("When both params are aware their timezones must match.")
            else:
                tzconvert = tzs[0]
                dt = dt.replace(tzinfo=timezone.utc).astimezone(tzconvert)
        check = from_dt <= dt <= to_dt
        if check:
            return True
        else:
            raise OutsidePermittedDatetime(f"This command can only run from {from_dt.strftime('%x %X')} "
                                           f"to {to_dt.strftime('%x %X')} timezone={dt.tzname()}")

    return commands.check(predicate)


def only_these_users(*users: int) -> commands.check:
    """
    Returns True under the following conditions:
        - ctx.author is authorized by this check

    .. warning::
        If no users are specified this command will be effectively unusable.

    Parameters
    ----------
        users: :class:`int`
            the ids of the user's that are authorized to use this command
    """

    def predicate(ctx):
        return ctx.author.id in users

    return commands.check(predicate)


def in_these_channels(*channels: int) -> commands.check:
    """
    Returns True under the following conditions:
        - **ctx.channel.id** is found within :param channels:

    .. warning::
        If no channels are specified this command will be effectively unusable

    Parameters
    ----------
        channels: :class:`int`
            One or more channel ids where this command can run
    """

    def predicate(ctx):
        return ctx.channel.id in channels

    return commands.check(predicate)


def is_guild_owner() -> commands.check:
    """
    Returns True under the following conditions:
        - **ctx.author** is the owner of the guild where this command was called from
    """

    def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command can only be used in a server.')
        author: Member = ctx.author
        if author != ctx.guild.owner.id:
            commands.MissingPermissions('This command can only be run by the owner of this guild.')

    return commands.check(predicate)


def any_checks(f: commands.Command):
    """Decorator to handle optional checks

    This Decorator will make any @checks placed below itself to be called with a logical OR.
    This means that if one or more return True, the command will be able to run

    .. note::

        When using this decorator remember that you don't need to call it::

            # correct
            @any_checks

            # incorrect
            @any_checks()

    Example
    -------
    ::

        from dpytools.checks import any_checks

        @commands.guild_only()       # This command must be called inside a server
        @any_checks                  # Place the decorator above the checks you with to compare using "OR"
        @commands.is_owner()         # The command will run if ctx.author is the owner of the bot
        @commands.has_role('Admin')  # __OR__ if ctx.author has the role "Admin"
        @bot.command()               # this decorator transforms this function in a command
        async def test(ct):
            await ctx.send('The command works')

    .. warning::

        This decorator makes it impossible to know which optional checks succeded or failed.

    .. note::

        The decorator will raise CheckFailure if all checks below itself fail

    Raises
    ------
        :class:`commands.CheckFailure`
            If all checks below itself fail.

    """

    if not isinstance(f, commands.Command):
        raise TypeError("This decorator must be placed above the @command decorator.")

    checks = copy(f.checks)

    async def async_any_checks(ctx):
        if len(checks) == 0:
            return True
        else:
            result = any([await _silent_except(c, ctx) for c in checks])
            if result:
                return True
            else:
                raise commands.CheckFailure(f'All optional checks for command "{f.qualified_name}" failed')

    f.checks = [async_any_checks]
    return f


def is_admin():
    """
    Shorthand for `@commands.has_guild_permissions(administrator=True)`
    """
    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command can only be used in a server.')
        if not ctx.author.guild_permissions.administrator:
            raise MissingPermissions('administrator')

        return True

    return commands.check(predicate)

## add is_admin
