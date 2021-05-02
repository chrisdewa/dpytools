# -*- coding: utf-8 -*-

"""
This module holds functions for displaying different kinds of menus.
All menus are reaction based.
"""

import asyncio
from typing import List, Optional, Union

import discord
from discord import Embed
from discord.ext import commands

__all__ = (
    "arrows",
    "confirm",
)

async def try_clear_reactions(msg):
    """helper function to remove reactions excepting forbidden
    either by context being a dm_channel or bot lacking perms"""

    if msg.guild:
        try:
            await msg.clear_reactions()
        except discord.errors.Forbidden:
            pass


async def arrows(ctx: commands.Context,
                 embed_list: List[Embed],
                 head: int = 0,
                 timeout: int = 30,
                 closed_embed: Optional[Embed] = None,
                 channel: Optional[discord.abc.Messageable] = None):
    """
    Sends multiple embeds with a reaction navigation menu.

    Args:
        ctx:
            The context where this function is called.
        embed_list  (List[Embed])
            An ordered list containing the embeds to be sent.
        head (int)
            The index in embed_list of the first Embed to be displayed.
        timeout (int: seconds)
            The time before the bot closes the menu.
            This is reset with each interaction.
        closed_embed (Optional[Embed]):
            The embed to be displayed when the user closes the menu.
            Defaults to plain embed with "Closed by user" in description

        channel (discord.abc.Messageable)
            The channel to be used for displaying the menu, defaults to ctx.channel.
    Returns:
        None
    """
    channel = channel or ctx.channel
    closed_embed = closed_embed or Embed(description="Closed by user")

    if len(embed_list) == 1:
        return await ctx.send(embed=embed_list[0])

    emojis = ['⏮', '◀', '▶', '⏭', '❌', '⏸']

    msg = await channel.send(embed=embed_list[head])

    for emoji in emojis:
        await msg.add_reaction(emoji)

    def check(payload):
        return all([
            payload.user_id == ctx.author.id,
            payload.emoji.name in emojis,
            msg.id == payload.message_id
        ])

    def return_head(head: int, emoji: str) -> Union[bool, int]:
        if emoji == '⏮':  # return to the first Embed
            return 0
        elif emoji == '◀':  # one left
            return head - 1 if head > 0 else 0
        elif emoji == '▶':  # one right
            return head + 1 if head < (len(embed_list) - 1) else len(embed_list) - 1
        elif emoji == '⏭':  # go to the end
            return len(embed_list) - 1
        elif emoji == '❌':  # close the menu
            return False
        elif emoji == '⏸':  # remove the reactions and keep the selected embed open.
            return True

    while True:
        try:
            payload = await ctx.bot.wait_for('raw_reaction_add', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            return await try_clear_reactions(msg)
        else:
            head = return_head(head, payload.emoji.name)
            if head is True:
                return await try_clear_reactions(msg)

            if head is False:
                await try_clear_reactions(msg)
                return await msg.edit(embed=closed_embed)

            elif isinstance(head, int):
                try:
                    await msg.remove_reaction(payload.emoji, ctx.author)
                except discord.errors.Forbidden:
                    pass

                await msg.edit(embed=embed_list[head])


async def confirm(ctx: commands.Context,
                  msg: discord.Message,
                  lock: Union[discord.Member, discord.Role, bool, None] = True,
                  timeout: int = 30) -> Optional[bool]:
    """Helps to create a reaction menu to confirm an action.
    :Parameters:
        ctx                    - the context for the menu
        msg                    - the message to confirm or deny by the user.
        lock                   -
            :Bool:             -
                True (default) - the menu will only listen for the author's reactions.
                False          - ANY user can react to the menu
            :discord.Member:   - only target member will be able to react
            :discord.Role:     - ANY user with target role will be able to react.
        timeout (seconds)      - Timeout before the menu closes.

    Returns:
        True if the message was confirmed
        False if it was denied
        None if timeout
    """

    emojis = ['👍', '❌']
    for emoji in emojis:
        await msg.add_reaction(emoji)

    def check(payload):
        _checks = [
            payload.user_id != ctx.bot.user.id,
            payload.emoji.name in emojis,
            payload.message_id == msg.id,
        ]
        if lock:
            if isinstance(lock, bool):
                _checks.append(payload.user_id == ctx.author.id)
            elif isinstance(lock, discord.Member):
                _checks.append(payload.user_id == lock.id)
            elif isinstance(lock, discord.Role):
                _checks.append(lock in ctx.guild.get_member(payload.user_id).roles)
        return all(_checks)

    try:
        payload = await ctx.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await try_clear_reactions(msg)
        return None
    else:
        await try_clear_reactions(msg)
        if payload.emoji.name == '👍':
            return True
        else:
            return False
