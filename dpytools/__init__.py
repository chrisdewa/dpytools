# -*- coding: utf-8 -*-
"""
Collection of uncategorized tools
"""
from enum import IntEnum
from inspect import isawaitable
from typing import List, Any, Callable

from .emojis import Emoji, EmojiNumbers

__title__ = 'dpytools'
__author__ = 'ChrisDewa'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 ChrisDewa'

__all__ = (
    'Color',
    'chunkify',
    'chunkify_string_list',
    '_silent_except'
)

class Color(IntEnum):
    """
    Enum class with nice color values that can be used directly on embeds

    Example::

        from dpytools import Color
        embed = discord.Embed(description="embed example", color=Color.FIRE_ORANGE)

    .. note::
        Available colors:
            CYAN = 0x00FFFF
            GOLD = 0xFFD700
            YELLOW = 0xffff00
            RED = 0xFF0000
            LIME = 0x00FF00
            VIOLET = 0xEE82EE
            PINK = 0xFFC0CB
            FUCHSIA = 0xFF00FF
            BLUE = 0x0000FF
            PURPLE = 0x8A2BE2
            FIRE_ORANGE = 0xFF4500
            COSMIC_LATTE = 0xFFF8E7
            BABY_BLUE = 0x89cff0

    """
    CYAN = 0x00FFFF
    GOLD = 0xFFD700
    YELLOW = 0xffff00
    RED = 0xFF0000
    LIME = 0x00FF00
    VIOLET = 0xEE82EE
    PINK = 0xFFC0CB
    FUCHSIA = 0xFF00FF
    BLUE = 0x0000FF
    PURPLE = 0x8A2BE2
    FIRE_ORANGE = 0xFF4500
    COSMIC_LATTE = 0xFFF8E7
    BABY_BLUE = 0x89cff0


def chunkify(input_list: List[Any],
             max_number: int
             ) -> List[List[Any]]:
    """
    Splits a list into :n: sized chunks

    Parameters
    ----------
    input_list: :class:`List[Any]`
        The list to make chunks from
    max_number: :class:`int`
        The maximum amount of items per chunk

    Yields
    ------
    Chunks of size equal or lower to *max_number*
    """
    for i in range(0, len(input_list), max_number):
        yield input_list[i:i + max_number]


def chunkify_string_list(input_list: List[str],
                         max_number: int,
                         max_length: int,
                         separator_length: int = 0
                         ) -> List[List[str]]:
    """
    Splits a list of strings into :param max_number: sized chunks or sized at maximum joint length of :param max_length:

    Parameters
    ----------
    input_list: :class:`List[str]`
        A list of strings
    max_number: :class:`int`
        Maximum amount of items per chunk
    max_length: :class:`int`
        Maximum amount of characters per chunk
    separator_length: :class:`int`
        If the strings will be eventually joined together, the :param separator_length:
        is considered into :param max_length:

    Yields
    ------
    :class:`List[List[str]]`
    """
    if any([len(item) > max_length - separator_length for item in input_list]):
        raise ValueError(f"All items should be of length {max_length} or less.")

    for i in range(0, len(input_list), max_number):
        n = max_number
        l = input_list[i:i + n]
        while len(''.join(opt + '_' * separator_length for opt in l)) - separator_length > max_length:
            n -= 1
            l = input_list[i:i + n]
        yield l


async def _silent_except(f: Callable, *args, **kwargs):
    """
    Helper Function that calls a function or coroutine and returns its result excepting all errors
    """
    try:
        called = f(*args, **kwargs)
    except:
        return
    if isawaitable(called):
        try:
            result = await called
        except:
            return
        else:
            return result
    else:
        return called
