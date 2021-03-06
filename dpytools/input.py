import asyncio
import re
from typing import Union, Optional, List

import discord
from discord.ext import commands


async def reply(ctx: commands.Context,
                expect: Optional[List[str]] = None,
                stop: str = 'cancel',
                timeout: Optional[int] = 30
                ) -> Union[discord.Message, bool, None]:
    """
    This function returns a user reply.
    Args:
        ctx: the command context
        expect: list of strings for options that are expected in the message string
        stop: string to stop this function
        timeout: time in seconds to wait for a reply or None if the function should wait forever (usual maximum is a day)

    Returns:
        None: if :timeout: is reached or if :stop: string is passed
        False: if there :expected: is passed and the user reply isn't a match for any.
        discord.Message: User's reply message.
    """

    def check(msg: discord.Message) -> bool:
        return msg.channel == ctx.channel and msg.author == ctx.author

    try:
        message = await ctx.bot.wait_for(
            'message',
            timeout=timeout,
            check=lambda msg: msg.channel == ctx.channel and msg.author == ctx.author
        )

    except asyncio.TimeoutError:
        return None

    else:
        if message.content.lower() == stop:
            return None

        elif expect:
            pattern = f"^(" + '|'.join(s for s in expect) + ")$"
            if not re.match(pattern, message.content, flags=re.I):
                return False

        return message
