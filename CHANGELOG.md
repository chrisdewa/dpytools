# 0.18.0b
- Reorganizing functions some tools
  - Emoji, EmojiNumbers and Embed will remain on their file but will be imported to `__init__`
  - As such they will be able to be accessed directly from dpytools

# 0.17.4b
- Fixed bug where **TextMenu** would start repeating its questions after the first call.
- Added property to **Embed** that tells you if the embed is valid (acording to the length limits of its fields and global character limit)

# 0.17.3b
- Fixed bug on **TextMenu** where messages would not be cleaned on timeout or cancel

# 0.17.2b
- Fixed **TextMenu** bug where the menu would ignore the stop string
- Documentation improvements

# 0.17.1b
- Improved **TextMenu** so `add_question` also accept `embed` and `parse_fail_embed`

# 0.17.0b
- **Upcoming braking change** emoji enums have been moved to `dpytools.emojis` at the moment __init__ imports 
the emojis, so it shouldn't break anything for now, however on a future version, this import might be deprecated
- Added `__all__` to all modules
- Added new menu `TextMenu`. Still in alpha. Probably not suitable for production yet.
- Added new check `is_admin` which is a shorthand for `@commands.has_guild_permissions(administrator=True)`

# 0.16.0b
- new check helper `@any_checks` that make checks below it be processed with a logical OR

# 0.15.7b
- added new embed tool `PaginatedEmbeds`

# 0.15.6b
- Documentation improvements
- `dpytools.embeds.Embed.add_fields` now returns the embed to make chaining easier

# 0.15.5b
- Documentation is live and can be accessed [here](https://dpytools.readthedocs.io/en/master/)

# 0.15.0b
- Introducing proper documentation
- General improvements
- **Breaking changes**:
  - Deprecating error class `Unauthorized`, substituted with `discord.ext.commands.MissingPermissions`

# 0.14.0b
- Started working on migrating docstrings from google format to RST for future formal documentation generation
- Minor bug fixes

# 0.13.0b
- Improved `arrows` with better emojis and logic
- Small bugfixes
- Improved Readme
- Refractor format and imports

# 0.11.1b
- Improved `MemberUserProxy`

# 0.11.0b
- Added new check `in_these_channels` by Kshitiz-Arya
- Added new parser `MemberUserProxy`
- Improved docs

# 0.10.0b
- Added new check `only_these_users`

# 0.9.0b
- Added a subclass of discord.Embed with added functionality

# 0.8.7b
- fix bug in arrows

# 0.8.2b-0.8.6b
- minor bug fixes and general improvements

# 0.8.1b
- bug fixes
- minor improvements

# 0.8.0b
- New general functions `chunkify` and `chunkify_string_list` and `EmojiNumbers`
- New menu tool `multichoice` (must check out!)
- Reformatted All.md because it was too hard to keep up with links


# 0.7.0b
- Improved readme
- Added some emojis
- Tested functions
- Development advanced to beta

# 0.6.0a
- new parser `to_month`

# 0.5.1a
- check `between_datetimes` can now handle aware datetime objects.
  - If the params are aware then ctx.message.created_at will be converted to that timezone for comparisons.

# 0.5.0a
- New checks `between_times` and `between_datetimes`

# 0.4.3a
- Minor documentation improvement
- new tool `dict_to_fields` in embeds

# 0.4.2a
- new colors
- Documentation improvements

# 0.4.1a
- Added All.md a list with all the tools in the library
- Minor fixes
- Potentially breaking change in `Trimmer` where `max_lenght` no longer has a default.

# 0.4.0a
- New check `this_or_higher_role`. Checks if user has a role or any higher than it.
- FAQ moved to /docs

# 0.3.0a
- Improved package description
- New Parser `Trimmer` callable class to convert a string to a certain maximum length
- Added new general tool `Color` IntEnum with Hex values for truly nice colors (more will be added)
- Added new general tool `Emoji` str Enum mixin with common emojis (more will be added)

# 0.2.1a
- Improved `latency` command
- Added F.A.Q.
- Improved Readme

# 0.0.21a 
- updated package dependencies

# 0.0.20a
- updated docstrings
- added parser `to_spongebob_case`
  present in the current guild or the command could be accessed from a direct message
- added check `any_of_permissions` a check to see if the ctx.author matches any selected permisisons (works like 'or') 


# 0.0.19a
- changed time_parser name to `to_timedelta`

# 0.0.18a
- improved time_parser output constructor

# 0.0.17a
- Added README badges
- Bug fixes and improvements in menus
- General code improvements for readability and mantainability

# 0.0.16a1
- Improved module documentation
- bug fix in `wait_for_regex`
- Fixed version error in PyPi

# 0.0.16a
- Expanded the documentation of various functions.

# 0.0.15a1
- renamed `user_interaction` to `waiters`
- Changed the name of `user_reply` to `wait_for_author`
- Added waiter `wait_for_regex`
- Changed the name of `parse_time` to `time_parser`
- Added command `latency`
- Added installation instructions to README.md
- Modified check `admin_or_roles` inner variable names

# 0.0.15a
- Renamed owner_cog to commands. 
  This was done because it makes more sense to import specific commands than the entire cog. 

# 0.0.14a 
- added two new parser functions to_upper and to_lower

# 0.0.13a
- new submodule "input" to get input from users
- new function `input.reply` to get specific reply from user

# 0.0.12a1
- checks.dm_from_this_guild now accepts aditional argument :delete: to remove the message if called from a guild. This will work only if it comes from the specified guild. If its a different guild the check will just return False


# 0.0.12a
- added check `checks.dm_from_this_guild` 

# 0.0.11a
- Improved cogs command from owner_cog

# 0.0.10a

- Added more proper documentation.