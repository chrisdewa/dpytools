[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![PyPI status](https://img.shields.io/pypi/status/dpytools.svg)](https://pypi.python.org/pypi/dpytools/)
[![PyPI version fury.io](https://badge.fury.io/py/dpytools.svg)](https://pypi.python.org/pypi/dpytools/)
[![Downloads](https://pepy.tech/badge/dpytools)](https://pepy.tech/project/dpytools)
[![PyPI license](https://img.shields.io/pypi/l/dpytools.svg)](https://pypi.python.org/pypi/dpytools/)


# dpytools
Collection of tools to speed up developing discord bots using discord.py

# Features
- The batteries of discord.py
- Easy to read type-hinted code
- Active development
- Minimal dependencies

# Instalation
Install the latest version of the library with pip.
```
pip install -U dpytools
```

# Useful links:
- [List](https://github.com/chrisdewa/dpytools/blob/master/docs/All.md) of all the tools.
- [Project Home](https://github.com/chrisdewa/dpytools) on github
- [Changelog](https://github.com/chrisdewa/dpytools/blob/master/CHANGELOG.md)
- [F. A. Q.](https://github.com/chrisdewa/dpytools/blob/master/docs/FAQ.md) and examples

# Use Examples:
The library has a couple of reaction menus that are really easy to use.
`dpytools.menus.arrows` takes a list of embeds and displays it using a reaction menu.
```python
@bot.command()
async def arrow_menu(ctx):
    """
    This command sends a list of embeds in a reaction menu with emojis aid in navigation
    """
    from dpytools.menus import arrows
    long_list_of_embeds = [discord.Embed(...), ...]
    await arrows(ctx, long_list_of_embeds)
```
There are multiple checks you can use directly on your commands
`dpytools.checks.admin_or_roles` takes any number of strings (Role names) and ints  (role ID) 
and checks if the person using the command has those roles or has administrator permissions. 
```python
from dpytools.checks import admin_or_roles
@bot.command()
@admin_or_roles('Moderator', 123456789)
async def moderation(ctx):
    ctx.send('Only admins and people witha a role named "Moderator" ' 
             'or with a role with id 123456789 can use this command')
```
There are also multiple argument parsers. Functions that convert a user's input to something more useful.
`dpytools.parsers.to_timedelta` takes a string in the format `<number>[s|m|h|d|w]` and returns a timedelta object
```python
from dpytools.parsers import to_timedelta
@bot.command()
@commands.guild_only()
async def mute(ctx, member: discord.Member, time: to_timedelta):
    await ctx.send(f"{member.mention} muted for {time.total_seconds()} seconds")
    mute_role = ctx.guild.get_role(1234567890)
    await member.add_roles(mute_role)
    await asyncio.sleep(time.total_seconds())
    await member.remove_roles(mute_role)
    await ctx.send(f"{member.mention} unmuted")
```
This argument parsers can also be used outside the context of `discord.ext.commands`
In the end most of them only take a string and return the appropriate object.
Only converter classes that inherit from `discord.ext.commands.Converter` require a command context to work.

There are many other tools available in the library, check them in [docs/All.md](https://github.com/chrisdewa/dpytools/blob/master/docs/All.md)

# Todos:
1. Adjust Menus to use buttons where it makes sense.
2. Add proper documentation

# Status of the project
Beta.
All functions have been tested but new tools are frequently added.
Breaking changes may come depending on changes on API or discord.
Use in production only after extensive testing.

# Contributing
Feel free to make a pull request or rise any issues.

# Contact
Message me on discord at **ChrisDewa#4552** if you have any questions, ideas or suggestions.
