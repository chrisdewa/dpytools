from enum import Enum

__all__ = (
    'Emoji',
    'EmojiNumbers'
)


class Emoji(str, Enum):
    """
    Enum class with common emojis used for reaction messages or related interactions

    Example::

        from dpytools import Emoji
        message.add_reaction(Emoji.SMILE)

    .. note::
        Included Emojis:
            SMILE = 🙂, THUMBS_UP = 👍, THUMBS_DOWN = 👎,

            HEART = ❤️,GREEN_CHECK = ✅, X = ❌,

            PROHIBITED = 🚫, FIRE = 🔥, STAR = ⭐,

            RED_CIRCLE = 🔴, GREEN_CIRCLE = 🟢, YELLOW_CIRCLE = 🟡,

            LAST_TRACK = ⏮️, REVERSE = ◀️, PLAY = ▶️,

            NEXT_TRACK = ⏭️, PAUSE = ⏸️, FIRST_PLACE_MEDAL = 🥇,

            SECOND_PLACE_MEDAL = 🥈, THIRD_PLACE_MEDAL = 🥉,

            ONE = 1️⃣, TWO = 2️⃣, THREE = 3️⃣,

            FOUR = 4️⃣, FIVE = 5️⃣, SIX = 6️⃣,

            SEVEN = 7️⃣, EIGHT = 8️⃣, NINE = 9️⃣,

            TEN = 🔟, ZERO = 0️⃣
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
    """
    Shortcut enum class that contains the number emojis from :class:`Emoji`
    """
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