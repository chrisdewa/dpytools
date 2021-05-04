# Tools included in the library:


## General: `from dpytools import ...`
1. [Color](https://github.com/chrisdewa/dpytools/blob/master/dpytools/__init__.py#L14):
   - IntEnum class. Contains hex values for specific common colors, specially for embeds
2. [Emoji](https://github.com/chrisdewa/dpytools/blob/master/dpytools/__init__.py#L36)
   - StrEnum class. Contains the string representation of discord default emojis 
      that are commonly used specially in reactions.


## Checks (Command checks): `from dpytools.checks import ...`
1. [admin_or_roles](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py#L28)
   - Returns `True` only if `ctx.author` has admin privileges or the specified role.
2. [only_this_guild](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py#L73)
   - Command will only be executed if `ctx.guild.id` matches specified id.
3. [dm_from_this_guild](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py#L92)
   - Restrict the command to direct messages but only from members of target guild (id)
4. [any_of_permissions](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py#L133)
   - Checks if `ctx.author` has any of the passed permissions.
5. [this_or_higher_role](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py#L167)
   - Checks if the top role of `ctx.author` is equal or higher than specified role (id)


## Commands (discord.ext.commands.command) `from dpytools.commands import ...`
1. [latency](https://github.com/chrisdewa/dpytools/blob/master/dpytools/commands.py#L20)
   - Returns plain embed with hearbeat and latency in ms.
   - Credit to [ComfortablyCoding](https://github.com/ComfortablyCoding)
2. [cogs](https://github.com/chrisdewa/dpytools/blob/master/dpytools/commands.py#L34)
   - Easy way to load, unload and reload cogs. 
   - Has `commands.is_owner` check


## menus (reaction menus) `from dpytools.menus import ...`
1. [arrows](https://github.com/chrisdewa/dpytools/blob/master/dpytools/menus.py#L31)
   - Takes a list of `discord.Embed` objects and displays it with a navigation menu.
   - Features:
      - pause (remove reactions keep embed)
      - next, previous, first, last
      - close button.
2. [confirm](https://github.com/chrisdewa/dpytools/blob/master/dpytools/menus.py#L116)
   - Takes a `discord.Message` and adds reactions to confirm or cancel.
   - If reaction is 👍 returns `True`
   - If reaction is ❌ returns `False`
   - If timeout is reached returns `None`


## parsers (discord.ext.commands.command argument converters) `from dpytools import ...`
1. [to_spongebob_case](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py#L34)
   - Takes a string argument and returns it with alternating caps
   - Input:`'Have a nice day'`, Output: `'hAvE A NiCe dAy'`
2. [to_upper](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py#L49)
   - Takes a string argument and returns it in caps
   - Input:`'Have a nice day'`, Output: `'HAVE A NICE DAY'`
2. [to_lower](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py#L61)
   - Takes a string argument and returns it in lower case
   - Input:`'HAVE A NICE DAY'`, Output: `'have a nice day'`
3. [to_timedelta](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py#L73)
   - Takes a string in the format `<number>[s|m|h|d]` and returns its equivalent timedelta object
   - Input: `'2h30m'`, Output: `timedelta(hours=2, minutes=30)`
4. [Trimmer](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py#L122)
   - Callable class. Constructor takes a `max_lenght` (int) parameter.
      The instance takes a string arguments and trims it to `max_lenght` if the string was longer than that
      an `end_sequence` (default `'...'`) is attached at the end removing that many additional characters.
      - `trimmer = Trimmer(50)` 
      - Input: `'this is a very long and boring text that should be trimmed for whatever reason'`
      - Output: `'this is a very long and boring text that should...'`


# waiters `from dpytools.waiters import ...`
1. [wait_for_regex](https://github.com/chrisdewa/dpytools/blob/master/dpytools/waiters.py#L73)
   - Waits for and returns a message that contains a match for the specified pattern
2. [wait_for_author](https://github.com/chrisdewa/dpytools/blob/master/dpytools/waiters.py#L118)
   - Returns a single message from ctx.author in ctx.channel, features a 'cancel' sequence


# embeds `from dpytools.embeds import ...`
1. [paginate_to_embeds](https://github.com/chrisdewa/dpytools/blob/master/embeds/dict_to_fields.py#L13)
   - Takes a long string and returns a list of embeds paginating the string.
   - Sets the footer to `{page_number}/{total_pages}`
2. [dict_to_fields](https://github.com/chrisdewa/dpytools/blob/master/embeds/dict_to_fields.py#L50)
   - Takes a dictionary where each pair of key/value sets acordingly the name and value of a field in the passed embed.
   - Credit to [fuyu78](https://github.com/fuyu78)


More to come...






