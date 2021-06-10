# -*- coding: utf-8 -*-
"""
Module that holds methods related to discord's bot client method `wait_for`
They're useful for retrieving information from users.
This functions and classes expect at least discord.Context
so they're have to be use with the commands extension.
"""

import asyncio
import re
from typing import Union, Optional

import discord
from discord.ext import commands

__all__ = (
    'wait_for_regex',
    'wait_for_author',
    'BaseLock'
)


class BaseLock:
    """
    Callable class to use with the :check: parameter in client.wait_for('message')
    The default behavior only requires to pass the context in the constructor and will perform these checks:
        `ctx.author == message.author and ctx.channel == message.channel`
    If channel is passed then it will check `channel == message.channel`
    If lock parameter is passed (differently than True) then it'll check the object against message.author.

    The constructor Raises ValueError if channel is not a GuildChannel when lock is type Role.
    """

    def __init__(self,
                 ctx: commands.Context,
                 channel: Union[discord.TextChannel,
                                discord.abc.PrivateChannel] = None,
                 lock: Union[discord.Role,
                             discord.User,
                             discord.Member,
                             bool] = True,
                 ):
        self.ctx = ctx
        self.channel = channel or ctx.channel
        if isinstance(lock, discord.Role) and not isinstance(self.channel, discord.TextChannel):
            raise ValueError(f":lock: parameter is a role but the target channel is not a guild TextChannel")
        self.lock = lock

    def __call__(self, message: discord.Message) -> bool:
        checks = [message.channel == self.channel]

        if self.lock is True:
            checks.append(self.ctx.author == message.author)
        elif isinstance(self.lock, discord.Role):
            checks.append(self.lock in self.ctx.author.roles)
        elif isinstance(self.lock, (discord.Member, discord.User)):
            checks.append(self.lock == self.ctx.author)

        return all(checks)


async def wait_for_regex(ctx: commands.Context,
                         pattern: str,
                         ignore_case: bool = False,
                         timeout: int = 30,
                         channel: Union[discord.TextChannel,
                                        discord.abc.PrivateChannel] = None,
                         lock: Union[discord.Role,
                                     discord.Member,
                                     bool] = True,
                         ) -> Optional[discord.Message]:
    """
    Waits for a message that contains a match for the passed :param pattern:

    Parameters
    ----------
    ctx: :class:`discord.ext.commands.Context`
        The command context
    pattern: :class:`str`
        Regex string to look in the message
    ignore_case: :class:`bool`
        Defaults to False. If True sets re.I as flag.
    timeout: :class:`int` (seconds)
        Time in seconds to wait for the appropriate message
    channel: `discord.TextChannel`
        The channel where the message should come from. Defaults to ctx.channel.
    lock:
        - :class:`discord.Role` -> Only members with this role can answer
        - :class:`discord.Member` -> only specified member can answer
        - :class:`bool`: True -> Only ctx.author can answer
        - :class:`bool`: False -> Anyone can answer as long as its in the correct channel within the timeout window

    Returns
    -------
    :class:`Optional[discord.Message]`
        Returns **None** if timeout is specified and reached
        and the rest of the checks arent passed or no match for the pattern is found

    """

    class Check(BaseLock):
        def __call__(self, msg):
            if super().__call__(msg):
                return re.match(pattern, msg.content, flags=re.I if ignore_case else 0)

    check = Check(ctx, channel, lock)

    try:
        message = await ctx.bot.wait_for('message', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        return
    else:
        return message


async def wait_for_author(ctx: commands.Context,
                          stop: str = 'cancel',
                          timeout: Optional[int] = 30,
                          ) -> Optional[discord.Message]:
    """
    This function returns a single message from ctx.author in ctx.channel.

    Parameters
    ----------
    ctx: :class:`discord.ext.commands.Context`
        the command context
    stop: :class:`str` (defaults to 'cancel')
        String to stop this function
    timeout: :class:`int` (seconds)
        time in seconds to wait for a reply or None if the function should wait forever (usual maximum is a day)

    Returns
    -------
    :class:`Optional[discord.Message]`
        The user's reply **message**.

        **None** if **timeout** is reached or if **stop** string is passed
    """
    try:
        message = await ctx.bot.wait_for('message', timeout=timeout, check=BaseLock(ctx))
    except asyncio.TimeoutError:
        return
    else:
        if message.content.lower() == stop:
            return
        else:
            return message

