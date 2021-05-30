# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 ChrisDewa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from enum import IntEnum, Enum
from typing import List, Any

__title__ = 'dpytools'
__author__ = 'ChrisDewa'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 ChrisDewa'
__version__ = '0.14.0b'


class Color(IntEnum):
    """
    Enum class with nice color values that can be used directly on embeds

    :Example:

    from dpytools import Color
    embed = discord.Embed(description="embed example", color=Color.FIRE_ORANGE)
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


class Emoji(str, Enum):
    """
    Enum class with common emojis used for reaction messages or related interactions

    :Example:

    from dpytools import Emoji
    message.add_reaction(Emoji.SMILE)
    """
    SMILE = '🙂'
    THUMBS_UP = '👍'
    THUMBS_DOWN = '👎'
    HEART = '❤️'
    GREEN_CHECK = '✅'
    X = '❌'
    PROHIBITED = '🚫'
    FIRE = '🔥'
    STAR = '⭐'
    RED_CIRCLE = '🔴'
    GREEN_CIRCLE = '🟢'
    YELLOW_CIRCLE = '🟡'
    LAST_TRACK = '⏮️'
    REVERSE = '◀️'
    PLAY = '▶️'
    NEXT_TRACK = '⏭️'
    PAUSE = '⏸️'
    FIRST_PLACE_MEDAL = '🥇'
    SECOND_PLACE_MEDAL = '🥈'
    THIRD_PLACE_MEDAL = '🥉'
    ONE = "1️⃣"
    TWO = "2️⃣"
    THREE = "3️⃣"
    FOUR = "4️⃣"
    FIVE = "5️⃣"
    SIX = "6️⃣"
    SEVEN = "7️⃣"
    EIGHT = "8️⃣"
    NINE = "9️⃣"
    TEN = "🔟"
    ZERO = "0️⃣"


class EmojiNumbers(str, Enum):
    """Shortcut enum class that contains the number emojis from :class:`Emoji`"""
    ONE = Emoji.ONE.value
    TWO = Emoji.TWO.value
    THREE = Emoji.THREE.value
    FOUR = Emoji.FOUR.value
    FIVE = Emoji.FIVE.value
    SIX = Emoji.SIX.value
    SEVEN = Emoji.SEVEN.value
    EIGHT = Emoji.EIGHT.value
    NINE = Emoji.NINE.value
    TEN = Emoji.TEN.value
    ZERO = Emoji.ZERO.value


def chunkify(input_list: List[Any],
             max_number: int
             ) -> List[List[Any]]:
    """
    Splits a list into :n: sized chunks

    Parameters:
        :param input_list: The list to make chunks from
        :param max_number: The maximum amount of items per chunk
    Yields:
        Chunks of size equal or lower to :param max_number:
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
    Yields:
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
