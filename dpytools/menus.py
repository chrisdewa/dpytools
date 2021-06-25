# -*- coding: utf-8 -*-

"""
This module holds functions for displaying different kinds of menus.
All menus are reaction based.
"""

import asyncio
from copy import copy
from inspect import isawaitable
from typing import List, Optional, Union, Callable

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context, Converter

from dpytools import EmojiNumbers, Emoji, chunkify_string_list, Color
from dpytools.errors import UserAnswerParsingError
from dpytools.waiters import BaseLock

__all__ = (
    'try_clear_reactions',
    'arrows',
    'confirm',
    'multichoice',
    'TextMenu'
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
                 content: Optional[str] = None,
                 head: int = 0,
                 timeout: int = 30,
                 closed_embed: Optional[Embed] = None,
                 channel: Optional[discord.abc.Messageable] = None):
    """
    Sends multiple embeds with a reaction navigation menu.

    Parameters
    ----------
    ctx: :class:`discord.ext.commands.Context`
        The context where this function is called.
    embed_list: :class:`List[Embed]`
        An ordered list containing the embeds to be sent.
    content: :class:`str`
        A static string. This wont change with pagination.
        It will be cleared when its closed, but will persist on pause
    head: :class:`int`
        The index in embed_list of the first Embed to be displayed.
    timeout: :class:`int` (seconds)
        The time before the bot closes the menu.
        This is reset with each interaction.
    closed_embed: :class:`Optional[Embed]`
        The embed to be displayed when the user closes the menu.
        Defaults to plain embed with "Closed by user" in description
    channel: :class:`discord.abc.Messageable`
        The channel to be used for displaying the menu, defaults to ctx.channel.

    Example
    -------
    ::

        from dpytools.menus import arrows
        @bot.command()
        async def test(ctx):
            embed_list = [Embed(...), Embed(...), ...)
            await arrows(ctx, embed_list)
    """
    channel = channel or ctx.channel
    closed_embed = closed_embed or Embed(description="Closed by user", color=Color.RED)

    if len(embed_list) == 1:
        return await channel.send(content=content, embed=embed_list[0])

    def get_reactions(_head: int):
        _to_react = []
        emb_range = range(len(embed_list))
        if _head - 2 in emb_range:
            _to_react.append(Emoji.LAST_TRACK.value)
        if _head - 1 in emb_range:
            _to_react.append(Emoji.REVERSE.value)
        if _head + 1 in emb_range:
            _to_react.append(Emoji.PLAY.value)
        if _head + 2 in emb_range:
            _to_react.append(Emoji.NEXT_TRACK.value)
        _to_react += [Emoji.PAUSE.value, Emoji.X.value]
        return _to_react

    msg = await channel.send(content=content, embed=embed_list[head])

    to_react = get_reactions(head)
    for emoji in to_react:
        await msg.add_reaction(emoji)

    def check(payload_):
        return all([
            msg.id == payload_.message_id,
            payload_.user_id == ctx.author.id,
            payload_.emoji.name in to_react,
        ])

    def get_head(head_: int, emoji_) -> Union[bool, int]:
        actions = {
            Emoji.LAST_TRACK: 0,
            Emoji.REVERSE: head_ - 1 if head_ else 0,
            Emoji.PLAY: head_ + 1 if head_ < len(embed_list) - 1 else len(embed_list),
            Emoji.NEXT_TRACK: len(embed_list) - 1,
            Emoji.X: False,
            Emoji.PAUSE: True,
        }
        return actions[emoji_]

    while True:
        try:
            payload = await ctx.bot.wait_for('raw_reaction_add', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            return await try_clear_reactions(msg)
        else:
            head = get_head(head, payload.emoji.name)
            if head is True:  # pause emoji triggered
                return await try_clear_reactions(msg)

            if head is False:  # X emoji triggered
                await try_clear_reactions(msg)
                return await msg.edit(content=None, embed=closed_embed, delete_after=10)

            else:
                await try_clear_reactions(msg)
                await msg.edit(embed=embed_list[head])
                to_react = get_reactions(head)
                for emoji in to_react:
                    await msg.add_reaction(emoji)


async def confirm(ctx: commands.Context,
                  msg: discord.Message,
                  lock: Union[discord.Member, discord.Role, bool, None] = True,
                  timeout: int = 30) -> Optional[bool]:
    """
    Helps to create a reaction menu to confirm an action.

    Parameters
    ----------
    ctx: :class:`discord.ext.commands.Context`
        the context for the menu
    msg: :class:`Message`
        the message to confirm or deny by the user.
    lock: :class:`Union[discord.Member, discord.Role, bool, None]`
        - **True** (default)
            - the menu will only listen for the author's reactions.
        - **False**
            - ANY user can react to the menu
        - :class:`discord.Member`
            - Only target member will be able to react
        - :class:`discord.Role`
            - ANY user with target role will be able to react.
    timeout: :class:ìnt` (seconds)
        Timeout before the menu closes.

    Returns
    -------
    :class:`Optional[bool]`
        - **True** if the message was confirmed
        - **False** if it was denied
        - **None** if timeout

    Example
    -------
    ::

        from dpytools.menus import confirm
        @bot.command()
        async def test(ctx):
            msg = await ctx.send('Please confirm to this important message')
            confirmation = await confirm(ctx, msg)
            if confirmation:
                await msg.edit(content='Confirmed')
            elif confirmation is False:
                await msg.edit(content='Cancelled')
            else:
                await msg.edit(content='Timeout')
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


async def multichoice(ctx: Context,
                      options: List[str],
                      timeout: int = 60,
                      base_embed: Embed = Embed()
                      ) -> Optional[str]:
    """
    Takes a list of strings and creates a selection menu.
    **ctx.author** will select and item and the function will return it.


    Parameters
    ----------
    ctx: :class:`Context`
        The command's context
    options: :class:`List[str]`
        List of strings that the user must select from
    timeout: :class:ìnt` (seconds)
        Timeout before the menu closes.
    base_embed: :class:`Optional[discord.Embed]`
        An optional embed object to take as a blueprint.
            - The menu will only modify the footer and description.
            - All other fields are free to be set by you.

    Example
    -------
    ::

        from dpytools.menus import multichoice
        @bot.command()
        async def test(ctx):
            options = [str(uuid4()) + for _ in range(110)]
            choice = await multichoice(ctx, options)
            await ctx.send(f'You selected: {choice}')

    Returns
    -------
        :class:`str`
            The item selected by the user.

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
        EmojiNumbers.TWO.value: 1,
        EmojiNumbers.THREE.value: 2,
        EmojiNumbers.FOUR.value: 3,
        EmojiNumbers.FIVE.value: 4,
        EmojiNumbers.SIX.value: 5,
        EmojiNumbers.SEVEN.value: 6,
        EmojiNumbers.EIGHT.value: 7,
        EmojiNumbers.NINE.value: 8,
        EmojiNumbers.TEN.value: 9,
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
            if head not in [0, len(embeds) - 1]:
                to_react = [Emoji.LAST_TRACK, Emoji.REVERSE] + to_react + [Emoji.PLAY, Emoji.NEXT_TRACK]
            elif head == 0:
                to_react = to_react + [Emoji.PLAY, Emoji.NEXT_TRACK]
            elif head == len(embeds) - 1:
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
                    next_embed.set_footer(text=f"Page {head + 1}/{len(embeds)}")
                    await msg.edit(embed=next_embed)
                    try:
                        await msg.clear_reactions()
                    except discord.errors.Forbidden:
                        pass
                    else:
                        to_react = get_reactions()
                        for reaction in to_react:
                            await msg.add_reaction(reaction)


class _QuestionData:
    """This class is not intended to be instantiated or subclassed"""
    def __init__(self,
                 *,
                 question: str = None,
                 embed: discord.Embed = None,
                 parser: Union[Converter, Callable, None] = None,
                 parse_fail_response: str = None,
                 parse_fail_embed: discord.Embed = None
                 ):
        self.failed = False

        if not question and not embed:
            raise ValueError('Either question or embed are required to construct the instance')

        self.question = question
        self.embed = embed
        self.parser = parser
        self.parse_fail_response = parse_fail_response
        self.parse_fail_embed = parse_fail_embed

    def __str__(self):
        return f"QuestionData(text={self.question})"


class TextMenu:
    """
    Constructs the menu instance

    Parameters
    ----------
        lock: **Union[discord.Member, discord.Role, bool, None]**
            - If **True** (default)
                - the menu will only listen for the author's reactions.
            - If **False**
                - ANY user can react to the menu
            - If **member**
                - Only target member will be able to react
            - If **role**
                - ANY user with target role will be able to react.
        stop: **str** (Default **'cancel'**)
            If the users passes this string in the message content the menu will end, clean up and return False
        timeout: **int** (Default **60**)
            The amount of time to wait for each question.
            If a timeout is reached, the menu is cancelled and cleaned up and returns None
        cleanup: **bool** (Default **True**)
            Whether to clean up messages or not

    .. note::

        If the users response matches the **stop** parameter the menu will return an explicit **False**

        If timeout occurs however return value will be **None**

        This way you can differentiate the output reasons

    """
    def __init__(self, *,
                 lock: Union[discord.Member, discord.Role, bool, None] = True,
                 stop: str = 'cancel',
                 timeout: int = 60,
                 cleanup: bool = False,
                 retry_parse_fail: bool = False,
                 ):
        self._questions: List[_QuestionData] = []
        self._messages = []
        self.lock = lock
        self.stop = stop
        self.timeout = timeout
        self.cleanup = cleanup
        self.retry_parse_fail = retry_parse_fail

    def add_question(self,
                     *,
                     question: str = None,
                     embed: discord.Embed = None,
                     parser: Union[Converter, Callable, None] = None,
                     parse_fail_response: str = None,
                     parse_fail_embed: discord.Embed = None,
                     ):
        """
        Adds a question to the menu

        Parameters
        ----------
            question: str
                The bot's question's text to display
            embed: discord.Embed
                An embed to send with the question
            parser: Union[Converter, Callable, None]
                - A function that takes a single string argument and returns something else
                    The function will be passed the user's message.content
                - Or a **discord.ext.commands.Converter**
                    Which will be given the same string and context from the command
            parse_fail_response: Optional[str]
                If the parser raises an exception and TextMenu .retry_parse_fail is enabled message content will be this
            parse_fail_embed: Optional[discord.Embed]
                If the parser raises an exception and TextMenu .retry_parse_fail is enabled message embed will be this

        .. warning::

            Either **question** or **embed** are required. If you dont pass any :class:`ValueError` will be raised

        """
        parse_fail_response = (parse_fail_response
                               or 'Failed to convert **"{}"** to desired type, try again'
                               if not parse_fail_embed else None)
        q = _QuestionData(question=question,
                          embed=embed,
                          parser=parser,
                          parse_fail_response=parse_fail_response,
                          parse_fail_embed=parse_fail_embed)
        self._questions.append(q)
        return self

    async def _try_to_clean(self, ctx: Context):
        """
        Tries to clean up messages excepting errors silently
        """
        if self.cleanup:
            try:
                await ctx.channel.delete_messages(self._messages)
            except:
                pass

    async def _ask(self, ctx, question: _QuestionData):
        """Asks an individual question"""
        check = BaseLock(ctx, lock=self.lock)
        msg_text = question.question if not question.failed else question.parse_fail_response
        msg_embed = question.embed if not question.failed else question.parse_fail_embed
        self._messages.append(await ctx.send(content=msg_text, embed=msg_embed))
        answer_msg = await ctx.bot.wait_for('message', check=check, timeout=self.timeout)
        self._messages.append(answer_msg)
        if answer_msg.content.lower().strip() == self.stop:
            return False
        if question.parser:
            try:
                if isinstance(question.parser, Converter):
                    answer = await question.parser.convert(ctx, answer_msg.content)
                elif isinstance(question.parser, type) and issubclass(question.parser, Converter):
                    answer = await question.parser().convert(ctx, answer_msg.content)
                else:
                    answer = question.parser(answer_msg.content)
                    if isawaitable(question.parser):
                        answer = await answer
            except Exception as e:
                question.failed = True
                question.parse_fail_response = (question.parse_fail_response.format(answer_msg.content)
                                                if question.parse_fail_response else None)
                raise UserAnswerParsingError(f"Failed to parse {question}") from e
        else:
            answer = answer_msg.content
        return answer

    async def call(self, ctx: commands.Context):
        """Activates the menu

        Displays the menu one question at the time.
        The user can cancel the menu using the :param stop: passed in the constructor
        The menu will only listen for messages that pass the base lock
        An attepmpt to clear all menu messages will be made with errors excepted silently

        Returns
        -------
            :class:`Optional[List[Any]]`
                Returns the list of answers from the user processed by the optional parser

                The menu will return None if a TimeoutError occurs.

        Raises
        ------
            :class:`Any`
                This menu will raise any exception derived from parsers
        """
        answers = []
        for question in self._questions:
            answer = None
            while answer is None:
                try:
                    answer = await self._ask(ctx, question)
                    if answer is False:
                        await self._try_to_clean(ctx)
                        return answer
                except asyncio.TimeoutError:
                    await self._try_to_clean(ctx)
                    return
                except UserAnswerParsingError as error:
                    if not self.retry_parse_fail:
                        await self._try_to_clean(ctx)
                        raise error
            answers.append(answer)

        await self._try_to_clean(ctx)
        return answers
