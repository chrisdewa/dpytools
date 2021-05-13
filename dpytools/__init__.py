# -*- coding: utf-8 -*-
"""
Uncategorized generic tools and utility functions
"""

from enum import IntEnum, Enum

__all__ = ('Color', 'Emoji', 'EmojiNumbers', 'chunkify', 'chunkify_string_list')

from typing import Iterable, List, Any


class Color(IntEnum):
    """
    Enum class with nice color values
    Can be used directly on embeds:
        ```
        embed = discord.Embed(description="embed example", color=dpytools.Color.FIRE_ORANGE)
        ```
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
    """Shortcut enum class that contains the number emojis from Emoji class"""
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


def chunkify(list_: List[Any],
             max_number: int
             ) -> List[List[Any]]:
    """
    Splits a list into :n: sized chunks
    Args:
        list_: a list
        max_number: an integer
    Yields:
        Chunks of :l: of :n: size
    """
    for i in range(0, len(list_), max_number):
        yield list_[i:i + max_number]


def chunkify_string_list(list_: List[str],
                         max_number: int,
                         max_length: int,
                         separator_length: int = 0
                         ) -> List[List[str]]:
    """
    Splits a list of strings into :max_number: sized chunks or sized at maximum joint length of :max_length:
    Args:
        list_: a list
        max_number (int): maximum number of items per chunk
        max_length (int): maximum length of characters in a chunk (considering all items)
        separator_length (int): Defaults to 0. If the strings will be eventually joined together this considers it
    Yields:
        List[List[str]]
    """
    if any([len(item) > max_length+separator_length for item in list_]):
        raise ValueError(f"All items should be of length {max_length} or less.")

    for i in range(0, len(list_), max_number):
        n = max_number
        l = list_[i:i + n]
        while len(''.join(opt + '_'*separator_length for opt in l))-separator_length > max_length:
            n -= 1
            l = list_[i:i + n]
        yield l
