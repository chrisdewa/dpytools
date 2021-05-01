# -*- coding: utf-8 -*-
"""
Uncategorized tools
"""

from enum import IntEnum, Enum

__all__ = [
    'Color',
    'Emoji',
]


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
    LAST_TRACK = '⏮'
    REVERSE = '◀'
    PLAY = '▶️'
    NEXT_TRACK = '⏭'
    PAUSE = '⏸'



