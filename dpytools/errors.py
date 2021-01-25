from discord.ext.commands import CommandError

class IncorrectGuild(CommandError):
    pass


class Unauthorized(CommandError):
    pass


class UnknownCog(CommandError):
    pass


class InvalidOption(CommandError):
    pass



