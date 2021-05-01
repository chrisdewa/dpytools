# -*- coding: utf-8 -*-
"""
This module holds functions to work with embeds in different ways.
"""

import discord
from discord import Embed
from discord.ext.commands import Paginator
from typing import List, Optional, Union


def paginate_to_embeds(title: str,
                       description: str,
                       max_size: int = 2000,
                       prefix: Optional[str] = "",
                       suffix: Optional[str] = "",
                       color: Union[discord.Color, int, None] = None
                       ) -> List[Embed]:
    """
    Facilitates sequential embed menus.
    Returned embeds share title, have description split at :max_length: and are added index/pages at footer to keep
    track of pages.

    Args:
        title: Shared by all embeds
        description: String to be split at :max_length: per embed.
        max_size: Maximum amount of characters per embed. Discord's limit is 2000.
        prefix: Defaults to "" it will be appended at the start of the description of each embed.
                Useful for codeblocks (use triple back quotes).
        suffix: Same as :prefix: but at the end of the text.
        color: color to use for the embed. Accepts int (decimal or hex) or discord.Color/discord.Colour.

    Returns:
        List[Embed]
    """
    embeds = []
    to_list = description.split("\n")
    paginator = Paginator(prefix=prefix, suffix=suffix, max_size=max_size)
    for line in to_list:
        paginator.add_line(line)
    for i, page in enumerate(paginator.pages):
        embeds.append(Embed(title=title,
                            description=page,
                            color=color, )
                      .set_footer(text=f"page: {i + 1}/{len(paginator.pages)}"))
    return embeds

