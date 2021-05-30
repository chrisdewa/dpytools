# -*- coding: utf-8 -*-
"""
This module holds functions to work with embeds in different ways.
"""

from typing import List, Optional, Union, Dict

import discord
from discord import Embed
from discord.ext.commands import Paginator
from datetime import datetime


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
        embed = Embed(description=page).set_footer(text=f"page: {i + 1}/{len(paginator.pages)}")
        d = {'title': title, 'colour': color}
        for attr in d:
            if value := d[attr]:
                setattr(embed, attr, value)

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

            
class EmbedList:
    
    """A class that takes dictionary containing name and value and splint them into several Embeds.

    Attributes
    -----------
    dicts: Optional[:class:`dict`]
        The dictionary containing name and values as key-value pair. Must not be empty
    title: Optional[:class:`str`]
        Title of the embeds. 
    description: :class:`int`
        Description of the embeds.
    footer: Optional[:class:`str`]
        Footer of the embeds
    author: Optional[:class:`str`]
        Author of the embeds
    inline: Optional[:class:`bool`]
        Bool variable if fields will be inline or not. Defaults to True
    size: Optional[:class:`int`]
        Number of field in each embed. Must be greater then 0. Defaults to 25
    color: Optional[:class:`discord.Color`, :class: `int`]
        The color of the disord embed. Default is Black
    """

    def __init__(self, **options):
        self.dicts = options.pop('dicts')
        self.title = options.pop('title', '')
        self.description = options.pop('description', '')
        self.footer = options.pop('footer', '')
        self.author = options.pop('author', '')
        self.inline = options.pop('inline', True)
        self.colour = options.pop('colour', 0)
        self.size = options.pop('size', 25)
        
        self.field_limit = 25
        self.char_limit = 6000
        self.clear()
        self._add_embed(self.dicts)

    def clear(self):
        """Clears the paginator to have no pages."""
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        """
        Check if the emebed is too big to be sent on discord

        Args:
            embed (discord.Embed): The embed to check

        Returns:
            bool: Will return True if the emebed isn't too large
        """
        check = (
            len(embed) + sum(len(char) for char in chars if char) < self.char_limit
            and len(embed.fields) < self.field_limit
        )
        return check

    def _new_page(self):
        """
        Create a new page

        Args:
            title (str): The title of the new page

        Returns:
            discord.Emebed: Returns an embed with the title and color set
        """
        return discord.Embed(title=self.title, description=self.description, timestamp=datetime.now(), color=self.colour)

    def _add_page(self, page: discord.Embed):
        """
        Add a page to the paginator

        Args:
            page (discord.Embed): The page to add
        """
        page.set_footer(text=self.footer)
        page.set_author(name=self.author)
        self._pages.append(page)

    def _chunks(self, dicts:dict):
        """Yield successive chunks of num size from dicts

        Args:
            dicts (dict): Dictionary containing name and value

        Yields:
            tuple_list (list): list chunks of size num containing name and value
        """        

        num = self.size
        if not dicts:
            raise ValueError("Dictionary containing name and value can't be empty!")

        tuple_list = [(name, value) for name, value in dicts.items()]

        if num < 1:
            raise ValueError("Number of Embed fields can't be zero")

        for i in range(0, len(tuple_list), num):
            yield tuple_list[i:i+num]
    
    def _add_embed(self, dicts):
        """Add embeds to pages

        Args:
            dicts :- Name, Value dictionary to generate embed from

        Returns:
            None

        """        
        for d in self._chunks(dicts):
            embed = self._new_page()

            for tup in d:
                name, value = tup
                embed.add_field(name=name, value=value, inline=self.inline)

            self._add_page(embed)

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        if len(self._pages) == 1:
            return self._pages
        lst = []
        for page_no, page in enumerate(self._pages, start=1):
            page: discord.Embed
            page.description = (
                f"`Page: {page_no}/{len(self._pages)}`\n{page.description}"
            )
            lst.append(page)
        return lst
