# -*- coding: utf-8 -*-
"""
Functions and classes used to convert :class:`str` into more useful classes.
This work very well with `discord.ext.commands` commands and can be used as typehints for arguments.
Function type parsers can work with any strings.

Function parameters are not generally documented here because they're the same, a **string**.

"""
import re
from datetime import timedelta
from typing import Tuple, Union

import discord.abc
from discord import NotFound, HTTPException
from discord.ext.commands import Converter, MemberConverter, UserConverter, MemberNotFound, UserNotFound, BadArgument

from dpytools.errors import InvalidTimeString

__all__ = (
    'to_spongebob_case',
    'to_upper',
    'to_lower',
    'to_timedelta',
    'Trimmer',
    'to_month',
    'MemberUserProxy',
)

def to_spongebob_case(string: str) -> str:
    """
    Converts a given string to spongebob case (alternating caps)

    Returns
    -------
    :class:`str`
        New string in sarcastic (spongebob) case
    """
    return ''.join(
        letter.upper() if i % 2 else letter.lower()
        for i, letter in enumerate(string)
    )


def to_upper(string: str) -> str:
    """
    Converts :string: to upper case. Intended to be used as argument converter.

    Returns
    -------
    :class:`str`
        String to upper case
    """
    return string.upper()


def to_lower(string: str) -> str:
    """
    Converts :string: to lower case. Intended to be used as argument converter.

    Returns
    -------
    :class:`str`
        string to lower case
    """
    return string.lower()


def to_timedelta(string: str) -> timedelta:
    """
    Converts a string with format <number>[s|m|h|d|w] to :class:`timedelta` object
    <number> must be convertible to float.

    Uses regex to match groups and consumes all groups into one timedelta.

    Units:
        - s: second
        - m: minute
        - h: hour
        - d: day
        - w: weeks

    Parameters
    ----------
        string: :class:`str`
            format <number>[s|m|h|d|w].

    Returns
    -------
    :class:`timedelta`
        the argument converted to a timedelta object

    Raises
    ------
        :class:`ValueError`
            If string number cannot be converted to float
        :class:`InvalidTimeString`:
            If string isn't in the valid form.

    Example
    -------
    ::

        from dpytools.parsers import to_timedelta
        @bot.command(name='time')
        async def _time(ctx, time: to_timedelta):
            print(time)

        # user's input: "2h30m"
        >>> timedelta(hours=2, minutes=30)

    """
    units = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks'
    }

    time_pattern = r"(\d+\.?\d?[s|m|h|d|w]{1})\s?"

    def parse(time_string: str) -> Tuple[str, float]:

        unit = time_string[-1]

        amount = float(time_string[:-1])
        return units[unit], amount

    if matched := re.findall(time_pattern, string, flags=re.I):
        time_dict = dict(parse(match) for match in matched)
        return timedelta(**time_dict)
    else:
        raise InvalidTimeString("Invalid string format. Time must be in the form <number>[s|m|h|d|w].")


class Trimmer:
    """
    Callable Class that trims strings to fit a maximum length

    Parameters
    ----------
        max_length: :class:`ìnt`
            Maximum length of the string
        end_sequence: :class:`str`
            Character sequence that denote that the full message is actually longer than the returned string
    """
    def __init__(self, max_length: int, end_sequence: str = '...'):
        self.max = max_length
        self.end_seq = end_sequence

    def __call__(self, string: str) -> str:
        """
        This turns the class into a callable object that parses the argument
        This is the actual parser

        Returns
        -------
        :class:`str`
            The processed string
        """
        string = string.strip()
        return string[: self.max - len(self.end_seq)].strip() + "..." if len(string) > self.max else string.strip()


def to_month(string: str) -> int:
    """
    This converter takes a string and checks if it contains a valid month of the year

    Parameters
    ----------
    string: :class:`str`
        Can be the full name, the shorter three leters conventional name or the number of the month

    Returns
    -------
    :class:`int`
        The number of the selected month

    Example
    -------
    ::

        from dpytools.parsers import to_month
        @bot.command(name='month')
        async def somemonth(ctx, month: to_month):
            print(month)

        # user's input: "jan"
        >>> 1
        # user's input "february"
        >>> 2
        # user's input "5"
        >>> 5
    """
    months = {
        1: ['january', 'jan'],
        2: ['february', 'feb'],
        3: ['march', 'mar'],
        4: ['april', 'apr'],
        5: ['may', 'may'],
        6: ['june', 'jun'],
        7: ['july', 'jul'],
        8: ['august', 'aug'],
        9: ['september', 'sep'],
        10: ['october', 'oct'],
        11: ['november', 'nov'],
        12: ['december', 'dec'],
    }
    error = ValueError(f'Argument "{string}" is not a valid month.')
    try:
        if (m := int(string)) in months:
            return m
    except ValueError:
        if m := next((k for k, v in months.items() if string.lower() in v), None):
            return m
        else:
            raise error
    else:
        raise error


class MemberUserProxy(Converter):
    """
    Tries to convert the argument first to :class:`discord.Member` and then to :class:`discord.User`,
    if it cannot be found returns :class:`discord.Object`


    If the bot cannot find the member or user object, the argument must be an id :class:`ìnt`.

    Returns
    -------
        :class:`Union[discord.Member, discord.User, discord.Object]`

    Raises
    ------
        BadArgument: if member or user cannot be found and and the argument cannot be converted to :class:`int`
    """

    async def convert(self, ctx, argument):
        """
        This does the actual conversion

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context that the argument is being used in.
        argument: :class:`str`
            The argument that is being converted.

        Raises
        -------
        :exc:`.CommandError`
            A generic exception occurred when converting the argument.
        :exc:`.BadArgument`
            The converter failed to convert the argument.
        """
        try:
            target = await MemberConverter().convert(ctx, argument)
        except MemberNotFound:
            try:
                target = await UserConverter().convert(ctx, argument)
            except UserNotFound:
                try:
                    _id = int(argument)
                except ValueError:
                    raise BadArgument('When user or member cannot be found you need to supply the id to build '
                                      'the proxy')
                try:
                    target = await ctx.bot.fetch_bot(_id)
                except (NotFound, HTTPException):
                    target = discord.Object(id=_id)
        return target
