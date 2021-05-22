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


class Embed(discord.Embed):
    def __init__(self, **kwargs):
        """
        Attributes
        ----------------------
        title:
            The title of the embed.
        type:
            The type of embed. Usually "rich".
            Official documentation states this is soon to be deprecated.
        description:
            The description of the embed.
        url:
            The URL of the embed.
        timestamp:
            The timestamp of the embed content. This could be a naive or aware datetime.
        colour (or color):
            The colour code of the embed.
        ----------------------
        Added by dpytools:
        ----------------------
        image:
            The image url
            Calls the internal "set_image" method with the kwarg value as the url
        thumbnail:
            The thumbnail url
            Calls the internal "set_thumbnail" method with the kwarg value as the url
        """
        super().__init__(**kwargs)
        if image := kwargs.get('image', None):
            self.set_image(url=image)

        if thumbnail := kwargs.get('thumbnail', None):
            self.set_thumbnail(url=thumbnail)

    def add_fields(self, inline=True, **kwargs):
        """
        Works in a similar way to Embed.add_field but you can add as many fields as you need by passing them as
        kwargs in the constructor.
        Example:
            embed = Embed()
            embed.add_fields(inline=False, first="this is the first field's value", second="Second field value")
        Note:
             If you need to add a sentence in the field's name just construct a dictionary and pass it with **.
             Example:
                 embed.add_fields(**{'first field': 'first field value'})
        Args:
            inline: if the fields will be inline or not
            **kwargs: key/value pairs for each field's name and value respectively
        """
        for name, value in kwargs.items():
            self.add_field(name=name, value=value, inline=inline)
