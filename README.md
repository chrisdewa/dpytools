# dpytools
Toolset to speed up developing discord bots using discord.py

<hr>

## Status of the project

Early development. As such its expected to be unstable and unsuited for production.

## Components
### menus
#### arrows
Displays a menu made from passed Embeds with navigation by reaction.
#### confirm 
Returns the user reaction to confirm or deny a passed message.

### embeds
#### paginate_to_embeds
Paginates a long text into a list of embeds.

### parsers
#### parse_time
Parses strings with the format "2h15m" to a timedelta object.

### owner_cog
Cog with different command useful for the owner of the bot
#### Commands
##### cogs 
lists, loads, unloads and reloads cogs in bulk or individually

### checks
#### admin_or_roles
Check if command user is an admin or has any of passed roles
#### only_this_guild
Check that limits the command to a specific guild.
#### dm_from_this_guild
Limits a command to direct messages while also checking if the user comes from a particular guild

<hr>

# Contributing
Feel free to make a pull request.