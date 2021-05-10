# 0.1.0b
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