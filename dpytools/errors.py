# -*- coding: utf-8 -*-
"""
This Module contains all custom errors used in the package.
"""
from discord.ext.commands import BadArgument, UserInputError

from discord.ext.commands import CommandError, CheckFailure


class NotMemberOfCorrectGuild(CommandError):
    pass


class IncorrectGuild(CommandError):
    pass


class Unauthorized(CommandError):
    pass


class InvalidOption(CommandError):
    pass


class InvalidTimeString(BadArgument):
    pass


class MemberNorUserFound(UserInputError):
    pass


class OutsidePermittedDatetime(CheckFailure):
    pass
