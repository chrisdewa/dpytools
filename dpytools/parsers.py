from datetime import timedelta
from typing import Dict
from collections import ChainMap
import re

class InvalidTimeString(Exception):
    pass

def parse_time(string: str) -> timedelta:
    """
    Converts a string with format <number>[s|m|h|d] to a timedelta object
    <number> must be convertible to float.
    Uses regex to match groups and consumes all groups into one timedelta.

    Units:
        s: second
        m: minute
        h: hour
        d: day

    Args:
        string: with format <number>[s|m|h|d].
            parse_time("2h") == timedelta(hours=2)

    Returns:
        timedelta

    Raises:
        ValueError: if string number cannot be converted to float
        InvalidTimeString: if string isn't in the valid form.

    """


    def parse(time_string: str) -> Dict:
        units = {'d': 'days', 's': 'seconds', 'm': 'minutes', 'h': 'hours', 'w': 'weeks'}

        unit = time_string[-1]

        amount = float(time_string[:-1])
        return {units[unit]: amount}

    pattern = r"(\d+[.]?\d?[s|m|h|d]{1})\s?"
    matched = re.findall(pattern, string)

    if not matched:
        raise InvalidTimeString("Invalid string format. Time must be in the form <number>[s|m|h|d].")

    time_dict = dict(ChainMap(*[parse(d) for d in matched]))

    return timedelta(**time_dict)
