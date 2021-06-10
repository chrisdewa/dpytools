# -*- coding: utf-8 -*-
"""
This module holds functions to work with embeds in different ways.
"""

from itertools import islice
from typing import List, Optional, Union, Dict

import discord
from discord import Embed
from discord.ext.commands import Paginator

__all__ = (
    'paginate_to_embeds',
    'dict_to_fields',
    'Embed',
    'PaginatedEmbeds',
)

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

    Parameters
    ----------
    description: :class:`str`
        String to be split at :max_length: per embed.
    title: :class:`str`
        Shared by all embeds
    max_size: :class:`int`
        Maximum amount of characters per embed. Discord's limit is 2000.
    prefix: :class:`str`
        Defaults to "" it will be appended at the start of the description of each embed.
        Useful for codeblocks (use triple back quotes).
    suffix: :class:`str`
        Same as :prefix: but at the end of the text.
    color: :class:`Union[discord.Color, int, None]`
        color to use for the embed. Accepts int (decimal or hex) or discord.Color/discord.Colour.

    Returns
    -------
    The rendered list of embeds :class:`List[Embed]`
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

    Parameters
    ----------
    embed:
        Instance of :class:`discord.Embed`
    fields: class`Dict[str, str]`
        Each key, value pair will be set as an independent field.
        They key corresponds to field.name and value to field.value.
    inline: :class:`bool`
        Specfiy whether if the fields should be inline or not. (Defaults to True)

    """
    for k, v in fields.items():
        embed.add_field(name=k, value=v, inline=inline)


class Embed(discord.Embed):
    """
    This is a subclass of :class:`discord.Embed` which accepts its default values plus image and thumbnail in the
    constructor and adds an additional method **add_fields**

    Parameters
    ----------
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
    image:
        The image url
        Calls the internal "set_image" method with the kwarg value as the url
    thumbnail:
        The thumbnail url
        Calls the internal "set_thumbnail" method with the kwarg value as the url
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if image := kwargs.get('image', None):
            self.set_image(url=image)

        if thumbnail := kwargs.get('thumbnail', None):
            self.set_thumbnail(url=thumbnail)

    def add_fields(self, inline=True, **kwargs) -> Embed:
        """
        Works in a similar way to **Embed.add_field** but you can add as many fields as you need by passing them as
        kwargs in the constructor.

        Parameters
        ----------
            inline: :class:`bool`
                if the fields will be inline or not
            kwargs:
                key/value pairs for each field's name and value respectively


        Example::

            from dpytools import Embed
            embed = Embed()
            embed.add_fields(inline=False, first="this is the first field's value", second="Second field value")

        .. note::

             If you need to add a sentence in the field's name just construct a dictionary and pass it with \*\*.

             Example::

                 embed.add_fields(**{'first field': 'first field value'})
        """
        for name, value in kwargs.items():
            self.add_field(name=name, value=value, inline=inline)
        return self


class PaginatedEmbeds:
    """A class that takes dictionary containing name and value as key-value pair and paginates them according to fields.

    Parameters
    -----------
    embed: :class:`Embed`
        Base Embed, which acts as a template for paginated embeds. This embed will have everything initiatized except fields.
    fields_dict: :class:`dict`
        The dictionary containing name and values as key-value pair. Must not be empty.
    size: Optional[:class:`int`]
        Number of field in each embed. Must be greater then 0. Defaults to 25.
    inline: Optional[:class:`bool`]
        Bool variable if fields will be inline or not. Defaults to True.
       
    Example
    -------
    ::
        
        from dpytools.embeds import PaginatedEmbeds
        from dpytools.menus import arrows
        @bot.command(name='send-fields')
        async def send_fields(ctx):
            lots_of_fields = {f'{i}': f'{i+1}' for i in range(1000)}
            pages = PaginatedEmbeds(Embed(title='Embed blueprint', color=0x00FFFF), lots_of_fields)
            await arrows(ctx, pages)

    .. warning::

        If parameter **embed** already has fields they will be cleared.
        Its suggested that the base embed has no fields before using this class.
        This will be issued in a coming update.

    """

    def __init__(self, embed: Embed, fields_dict: Dict[str, str], size: int = 25, inline: bool = True):
        embed.clear_fields()  # Clearing the fields just in case embed is not empty
        self.embed = embed
        self.size: int = size
        self.fields_dict = fields_dict
        self.inline: bool = inline

        self.field_limit = 25
        self.char_limit = 6000
        self._pages = []
        self._add_embed(self.fields_dict)

    def _clear(self):
        """Clears the paginator to have no pages."""
        self._pages = []

    def _check_embed(self, embed: Embed, *chars: str):
        """
        Check if the embed is too big to be sent on discord

        Parameters
        ----------
            embed: :class:`Embed`: 
                The embed to check

        Returns
        -------
            :class:`bool`
                Will return **True** if the emebed isn't too large
        """
        check = (
                len(embed) + sum(len(char) for char in chars if char) < self.char_limit
                and len(embed.fields) < self.field_limit
        )
        return check

    def _new_page(self) -> Embed:
        """
        Create a new page

        Returns:
            Embed: Return a new Embed for new page
        """
        return Embed.from_dict(self.embed.to_dict())  # This convert discord.Embed to Embed and return it

    def _add_page(self, page: Embed):
        """
        Add a page to the paginator

        Parameters
        ----------
            page: :class:`Embed`
                The page to add
        """

        self._pages.append(page)

    def _chunks(self, fields_dict: Dict[str, str]) -> Dict[str, str]:
        """Yield successive chunks of num size from dicts

        Args:
            fields_dict (dict): Dictionary containing name and value as key-value pair

        Yields:
            dict: dictionary with size :param num: containing name and value of each field
        """

        num = self.size
        if not fields_dict:
            raise ValueError("Dictionary containing name and value can't be empty!")

        if num < 1:
            raise ValueError("Number of Embed fields can't be zero")

        field_iter = iter(fields_dict)
        for _ in range(0, len(fields_dict), num):
            yield {k: fields_dict[k] for k in islice(field_iter, num)}

    def _add_embed(self, fields_dict: dict):
        """Add embeds to pages

        Args:
            fields_dict :- Dictionary containing name and value as key-value pair
        """
        for field_dict_chunk in self._chunks(fields_dict):
            field_dict_chunk: dict  # just to appease the linter
            embed = self._new_page()

            embed.add_fields(**field_dict_chunk)  # dict should be passed as kwargs or it will be taken as bool
            self._add_page(embed)

    @property
    def pages(self):
        """Returns the rendered list of pages"""
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
