# -*- coding: utf-8 -*-
"""
Cog with common functionality for bot owners.
"""

from discord.ext import commands
from discord.ext.commands import ExtensionError
from discord import Embed, Color
from typing import Optional
import os

from dpytools.errors import InvalidOption, UnknownCog


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("This command can only be executed by the owner of the bot")
        else:
            return True

    @commands.command(hidden=True)
    async def cogs(
            self,
            ctx: commands.Context,
            option: Optional[str],
            cog: Optional[str],
            cogs_dir: str = "./cogs"):
        """
        Command to load, unload and reload extensions.
        Args:
            ctx: commands.Context
            option:
                load: loads :cog:
                unload: unloads :cog:
                reload: relaods :cog:
                list: lists available cogs in :cogs_dir:
            cog: filename of the extension to load, without the file extension ('my_cog' not 'my_cog.py')
            cogs_dir: directory to operate command, defaults to ./cogs

        Raises:
            InvalidOption if option is not recognized
            UnknownCog if cog name is not found within the specified directory
        """
        if option.lower() not in ['load', 'unload', 'reload', 'list']:
            raise InvalidOption(f"{option} is not valid. Valid options are:'load', 'unload', 'reload' and 'list' ")

        bot = ctx.bot

        actions = {
            'load': bot.load_extension,
            'unload': bot.unload_extension,
            'reload': bot.reload_extension
        }

        cogs = [filename[:-3] for filename in os.listdir(cogs_dir) if filename.endswith('.py')]

        if option.lower() == 'list':
            await ctx.send(embed=Embed(
                title="Available cogs:",
                description="".join(f"{i + 1}) {cog}\n" for i, cog in enumerate(cogs)),
                color=Color.blue()
            ))
        else:
            action = actions[option]

            if cog.lower() == 'all':
                msg = await ctx.send(f'Doing: {action.__name__} on all')
                for cog in cogs:
                    try:
                        action(f"{cogs_dir[2:]}.{cog}")
                    except ExtensionError:
                        pass
            elif cog not in cogs:
                raise UnknownCog(f"{cog} is not a valid cog, check spelling and verify directory.")
            else:
                msg = await ctx.send(f'Doing: {action.__name__} on {cog}')
                action(f"{cogs_dir[2:]}.{cog}")

            await msg.edit(content=f'**Done!**')
