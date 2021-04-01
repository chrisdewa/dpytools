# 0.0.15a1
- Changed name of `user_reply` to `wait_for_reply`
- Changed name of `parse_time` to `time_parser`
- Added command `latency`
- Added instalation instructions to README.md
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