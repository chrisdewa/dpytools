import discord, asyncio
from discord.ext import commands
from discord import Embed
from typing import List, Optional, Union


async def clear(msg):
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
                 channel: Optional[discord.abc.Messageable] = None):
    """Sends multiple embeds with a reaction navigation menu.
    Intended to be used with discord.ext.commands

    :Parameters:
        ctx               - the context where this function is called.
        embed_list        - an ordered list containing the embeds to be sent.
        head              - the index in embed_list of the first Embed to be displayed.
        timeout (seconds) - the time before the bot closes the menu. This is reset with each interaction.
        channel           - the channel to be used for displaying the menu, defaults to ctx.channel.

    Returns:
        None
    """
    
    if not channel:
        channel = ctx.channel
    if len(embed_list) == 1:
        await ctx.send(embed=embed_list[0])
        return
    emojis = ['⏮', '◀', '▶', '⏭', '❌', '⏸']
    msg = await channel.send(embed=embed_list[head])
    for emoji in emojis:
        await msg.add_reaction(emoji)

    def check(payload):
        return payload.user_id == ctx.author.id and payload.emoji.name in emojis and msg.id == payload.message_id

    def return_head(head, emoji):
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
            return None

    head = head

    while True:
        try:
            payload = await ctx.bot.wait_for('raw_reaction_add', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            try:  # This is done so that if the menu is called in a dm_channel context it omits deleting the reactions.
                await msg.clear_reactions()
            except discord.errors.Forbidden:
                pass
            break
        else:
            head = return_head(head, payload.emoji.name)

            if head is False:
                await clear(msg)
                await msg.edit(embed=discord.Embed(description='Closed by user.'))

            elif isinstance(head, int):
                try:
                    await msg.remove_reaction(payload.emoji, ctx.author)
                except discord.errors.Forbidden:
                    pass

                emb = embed_list[head]
                await msg.edit(embed=emb)

            elif head is None:
                await clear(msg)
                break


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
        await clear(msg)
        return None
    else:
        await clear(msg)
        if payload.emoji.name == '👍':
            return True
        else:
            return False
