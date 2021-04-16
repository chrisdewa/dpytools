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