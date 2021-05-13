# -*- coding: utf-8 -*-

"""
This module holds functions for displaying different kinds of menus.
All menus are reaction based.
"""

import asyncio
from copy import copy
from typing import List, Optional, Union

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from dpytools import EmojiNumbers, Emoji, chunkify_string_list

__all__ = (
    "arrows",
    "confirm",
    "multichoice"
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


async def multichoice(ctx: Context,  # the command's context
                      options: List[str],  # a list with strings to present the user
                      timeout: int = 60,  # a timeout before each interaction before the embed closes
                      base_embed: Embed = Embed()  # an optional base embed for each pagination
                      ) -> Optional[str]:
    """
    Takes a list of strings and creates a selection menu.
    The ctx.author will select and item and the function will return it.
    Args:
        ctx: Command Context
        options: list of strings that the user must select from
        timeout: maximum time to wait before canceling (returns None)
        base_embed: an optional embed object to take as a blueprint.
            The menu will only modify the footer and description.
            All other fields are free to be set by you.
    Returns:
        str: the item selected by the user
    """
    if not options:
        raise ValueError("Options cannot be empty")
    elif (t := type(options)) is not list:
        raise TypeError(f'"options" param must be :list: but is {t}')
    elif not all([type(item) is str for item in options]):
        raise TypeError(f'All of the "options" param contents must be :str:')
    elif any([len(opt) > 2000 for opt in options]):
        raise ValueError("The maximum length for any option is 2000")

    multiple = len(options) > 10
    head = 0
    embeds = []
    nums = {
        EmojiNumbers.ONE.value: 0,
        EmojiNumbers.TWO.value:  1,
        EmojiNumbers.THREE.value:  2,
        EmojiNumbers.FOUR.value:  3,
        EmojiNumbers.FIVE.value:  4,
        EmojiNumbers.SIX.value:  5,
        EmojiNumbers.SEVEN.value: 6,
        EmojiNumbers.EIGHT.value:  7,
        EmojiNumbers.NINE.value:  8,
        EmojiNumbers.TEN.value:  9
    }

    for i, chunk in enumerate(chunkify_string_list(options, 10, 2000, separator_length=10)):
        description = "".join(f"{list(nums)[i]} {opt.strip()}\n\n" for i, opt in enumerate(chunk))
        embed = copy(base_embed)
        embed.description = description
        embeds.append((chunk, embed))

    def get_nums(_chunk):
        return list(nums)[:len(_chunk)]

    def get_reactions():
        to_react = get_nums(embeds[head][0])
        if multiple:
            if head not in [0, len(embeds)-1]:
                to_react = [Emoji.LAST_TRACK, Emoji.REVERSE] + to_react + [Emoji.PLAY, Emoji.NEXT_TRACK]
            elif head == 0:
                to_react = to_react + [Emoji.PLAY, Emoji.NEXT_TRACK]
            elif head == len(embeds)-1:
                to_react = [Emoji.LAST_TRACK, Emoji.REVERSE] + to_react
        return to_react + [Emoji.X]

    def adjust_head(head_: int, emoji: str):
        if not multiple:
            return
        else:
            if emoji == Emoji.LAST_TRACK:
                head_ = 0
            elif emoji == Emoji.REVERSE:
                head_ -= 1 if head_ > 0 else 0
            elif emoji == Emoji.PLAY:
                head_ += 1 if head_ < len(embeds) - 1 else 0
            elif emoji == Emoji.NEXT_TRACK:
                head_ = len(embeds) - 1
        return head_

    def check(reaction: discord.Reaction,
              user: Union[discord.User, discord.Member]):

        return all([
            user != ctx.bot.user,
            user == ctx.author,
            ctx.channel == reaction.message.channel,
            reaction.emoji in to_react,
        ])

    to_react = get_reactions()
    first_embed = embeds[0][1]
    first_embed.set_footer(text=f"Page 1/{len(embeds)}")
    msg = await ctx.send(embed=first_embed)

    for reaction in to_react:
        await msg.add_reaction(reaction)

    while True:
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            await msg.delete()
            return
        else:
            emoji = reaction.emoji
            if emoji == Emoji.X:
                await msg.delete()
                return
            else:
                if emoji in nums:
                    await msg.delete()
                    return embeds[head][0][nums[emoji]]
                else:
                    head = adjust_head(head, emoji)
                    next_embed = embeds[head][1]
                    next_embed.set_footer(text=f"Page {head+1}/{len(embeds)}")
                    await msg.edit(embed=next_embed)
                    try:
                        await msg.clear_reactions()
                    except discord.errors.Forbidden:
                        pass
                    else:
                        to_react = get_reactions()
                        for reaction in to_react:
                            await msg.add_reaction(reaction)
