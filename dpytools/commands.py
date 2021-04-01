# -*- coding: utf-8 -*-
"""
Common general purpose commands

Add them to your bot by simply doing
    ```
        bot.add_command(command)
    ```
"""

import os
from typing import Optional

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import ExtensionError



@commands.command(aliases=['lat'])
async def latency(ctx: commands.Context):
    """
    Command to disply latency in ms.
    Latency is displayed on plain embed in the description field
    Args:
        ctx: discord.Context

    Returns:
        None
    """
    await ctx.send(embed=Embed(
        description=f"Latency: {round(ctx.bot.latency * 1000, 1)}ms"
    ))


@commands.command(hidden=True)
@commands.is_owner()
async def cogs(ctx: commands.Context,
               option: Optional[str],
               cog: Optional[str],
               cogs_dir: str = "./cogs"):
    """
    Command to load, unload and reload extensions.

    Checks:
        commands.is_owner

    Attributes:
        hidden=True

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
