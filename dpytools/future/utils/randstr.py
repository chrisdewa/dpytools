import random
from string import ascii_letters

__all__ = (
    'randstr',
)

_abc = ascii_letters + '0123456789'


def randstr(length=5, chars=None):
    """
    Generates a random alphanumeric string with the given length.

    Parameters
    ----------
        length: :class:`int`: the maximum length of the generated string
        chars: :class:`string`: a string with unique characters to use for generating the string
            default: a-zA-Z0-9

    Returns
    -------
        :class:`str`: The generated string

    ..note::

        **This function does not guarantee that there won't be collisions**
        If collision prevention is required you should use the `uuid` module
        instead
    """
    chars = [*{ele for ele in (chars or _abc)}]
    return ''.join(random.choices(chars, k=length))
