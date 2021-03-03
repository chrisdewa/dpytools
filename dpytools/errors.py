# -*- coding: utf-8 -*-
"""
This Module contains all custom errors used in the package.
"""

from discord.ext.commands import CommandError

class NotMemberOfCorrectGuild(CommandError):
    pass


class IncorrectGuild(CommandError):
    pass


class Unauthorized(CommandError):
    pass

class InvalidOption(CommandError):
    pass
