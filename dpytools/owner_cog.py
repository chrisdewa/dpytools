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

        """
        if option.lower() not in ['load', 'unload', 'reload', 'list']:
            await ctx.send(embed=Embed(
                description=f"{option} is not valid. Valid options are:'load', 'unload', 'reload' and 'list' "))

        bot = ctx.bot

        actions = {
            'load': bot.load_extension,
            'unload': bot.unload_extension,
            'reload': bot.reload_extension
        }

        cogs = [found_cog for dp, dn, fn in
                os.walk(os.path.expanduser(cogs_dir)) for f in fn
                if '__pycache__' not in (found_cog := os.path.join(dp, f)
                                         .replace(cogs_dir, '')
                                         .replace('\\', '.')
                                         .replace('/', '.')[1:-3])]

        if option.lower() == 'list':
            await ctx.send(embed=Embed(
                title="Available cogs:",
                description="".join(f"{i + 1}) {cog}\n" for i, cog in enumerate(cogs)),
                color=Color.blue()
            ))
        else:
            action = actions[option]

            if cog.lower() == 'all':
                msg = await ctx.send(embed=Embed(description=f'Performing: {action.__name__} on all extensions'))
                for cog in cogs:
                    try:
                        action(f"{cogs_dir[2:]}.{cog}")
                    except ExtensionError as E:
                        await msg.edit(embed=Embed(description=f"Action could not be completed.\n"
                                                               f"Reason:\n"
                                                               f"```{E}```"))
                    else:
                        await msg.edit(embed=Embed(description=f'**Done!**'))
            elif cog not in cogs:
                await ctx.send(embed=Embed(
                    description=f"{cog} is not a valid cog, check spelling and verify directory."))
            else:
                msg = await ctx.send(embed=Embed(description=f'Performing: {action.__name__} on {cog}'))
                try:
                    action(f"{cogs_dir[2:]}.{cog}")
                except ExtensionError as E:
                    await msg.edit(embed=Embed(description=f"Action could not be completed.\n"
                                                           f"Reason:\n"
                                                           f"```{E}```"))
                else:
                    await msg.edit(embed=Embed(description=f'**Done!**'))
