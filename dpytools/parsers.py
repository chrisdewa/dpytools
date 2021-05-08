# -*- coding: utf-8 -*-
"""
This module holds parsers and converters to use with user input
Functions here can be used as type hints which discord.py will use as
custom converters or they can be used as regular functions.
Example:
    ```
    from dpytools.parsers import to_timedelta
    @bot.command()
    async def timedelta(ctx, time: to_timedelta):
        await ctx.send(f"time delta is: {time}")
    ```
    above command will be called like this: `!timedelta 2h30m`
    and it will send a message with "time delta is: 2:30:00"

    This way you don't have to manually parse the time string to a timedelta object.
    the parameter "time" will be of type timedelta.
"""
import re
from datetime import timedelta
from typing import Tuple, Union

from discord.ext.commands import ArgumentParsingError

from dpytools.errors import InvalidTimeString

__all__ = (
    'to_spongebob_case', 'to_upper',
    'to_lower',
    'to_timedelta',
    'Trimmer',
    'to_month',
)


def to_spongebob_case(string: str) -> str:
    """
    converts a given string to spongebob case (alternating caps)
    Args:
        string: the string to convert

    Returns:
        new string in sarcastic case
    """
    return ''.join(
        letter.upper() if i % 2 else letter.lower()
        for i, letter in enumerate(string)
    )


def to_upper(string: str) -> str:
    """
    Converts :string: to upper case. Intended to be used as argument converter.
    Args:
        string: string to format

    Returns:
        string to upper case
    """
    return string.upper()


def to_lower(string: str) -> str:
    """
    Converts :string: to lower case. Intended to be used as argument converter.
    Args:
        string: string to format

    Returns:
        string to lower case
    """
    return string.lower()


def to_timedelta(string: str) -> timedelta:
    """
    Converts a string with format <number>[s|m|h|d] to a timedelta object
    <number> must be convertible to float.
    Uses regex to match groups and consumes all groups into one timedelta.

    Units:
        s: second
        m: minute
        h: hour
        d: day
        w: weeks

    Args:
        string: with format <number>[s|m|h|d].
            parse_time("2h") == timedelta(hours=2)

    Returns:
        timedelta

    Raises:
        ValueError: if string number cannot be converted to float
        InvalidTimeString: if string isn't in the valid form.

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
    def __init__(self, max_length: int, end_sequence: str = '...'):
        """

        Args:
            max_length (int): maximum length of the string
            end_sequence (str): character sequence that
                denote that the full message is actually longer than the returned string
        """
        self.max = max_length
        self.end_seq = end_sequence

    def __call__(self, string: str) -> str:
        """
        This turns the class into a callable object that parses the argument
        Args:
            string: user text string

        Returns:
            (str) the passed string.
                If longer than max length it will be trimmed and :end_sequence: attached at the end.
        """
        string = string.strip()
        return string[: self.max - len(self.end_seq)].strip() + "..." if len(string) > self.max else string.strip()


def to_month(string: Union[str, int]) -> int:
    """
    This converter takes a string and checks if it contains a valid month.
    If the argument is the months name check is case insensitive
    returns the month number (int)
    Formats:
        January/jan/1
    Args:
        string: the string to parse
    Raises:
        ValueError if argument is not a valid month
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
    try:
        if (m := int(string)) in months:
            return m
    except ValueError:
        if m := next((k for k, v in months.items() if string.lower() in v), None):
            return m
        else:
            raise ValueError(f'Argument "{string}" is not a valid month.')
