# -*- coding: utf-8 -*-
"""
This module holds functions to work with embeds in different ways.
"""

from typing import List, Optional, Union, Dict

import discord
from discord import Embed
from discord.ext.commands import Paginator


def paginate_to_embeds(description: str,
                       title: Optional[str] = None,
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
        description: String to be split at :max_length: per embed.
        title: Shared by all embeds
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
        embed = Embed(description=page,
                      color=color).set_footer(text=f"page: {i + 1}/{len(paginator.pages)}")
        if title:
            embed.title = title
        embeds.append(embed)
    return embeds


def dict_to_fields(embed: Embed,
                   fields: Dict[str, str],
                   inline: bool = False) -> None:
    """
    Iterates through dict keys and appends them to the embed fields
    Args:
        embed: Embed instance
        fields (dict): each key, value pair will be set as an independent field.
            They key corresponds to field.name and value to field.value.
        inline: Specfiy whether if the fields should be inline or not. (Defaults to True)

    """
    for k, v in fields.items():
        embed.add_field(name=k, value=v, inline=inline)
