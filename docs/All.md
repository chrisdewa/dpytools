# Tools included in the library:


## [General](https://github.com/chrisdewa/dpytools/blob/master/dpytools/__init__.py): 
### `from dpytools import ...`
1. **Color**:
   - IntEnum class. Contains hex values for specific common colors, specially for embeds
2. **Emoji**:
   - StrEnum class. Contains the string representation of discord default emojis 
      that are commonly used specially in reactions.
3. **chunkify**:
   - function that returns chunks of :n: size from a list
4. **chunkify_string_list**:
   - Splits a list of strings into :max_number: sized chunks or sized at maximum joint length of :max_length:
5. **EmojiNumbers**:
   - Enum class with number emoji


## [Checks](https://github.com/chrisdewa/dpytools/blob/master/dpytools/checks.py) (Command checks): 
### `from dpytools.checks import ...`
1. **admin_or_roles**:
   - Returns `True` only if `ctx.author` has admin privileges or the specified role.
2. **only_this_guild**:
   - Command will only be executed if `ctx.guild.id` matches specified id.
3. **dm_from_this_guild**:
   - Restrict the command to direct messages but only from members of target guild (id)
4. **any_of_permissions**:
   - Checks if `ctx.author` has any of the passed permissions.
5. **this_or_higher_role**:
   - Checks if the top role of `ctx.author` is equal or higher than specified role (id)
6. **between_times**:
   - Checks if `ctx.message.created_at.time()` is in the specified interval
7. **between_datetime**:
   - Checks if `ctx.message.created_at` is in the specified interval
8. **only_these_users**:
   - Checks if ctx.author's id is authorized to run command.
9. **in_these_channels**:
   - Checks if ctx.channel is in the approved list
   - Credit to [Kshitiz-Arya](https://github.com/Kshitiz-Arya)
10. **is_guild_owner**:
   - As the name implies, it checks if `ctx.author` is the owner of the guild. 
11. **any_checks**:
   - A simple decorator that makes any checks below it be processed with a logical **OR**


## [Commands](https://github.com/chrisdewa/dpytools/blob/master/dpytools/commands.py) (discord.ext.commands.command)
### `from dpytools.commands import ...`
1. **latency**:
   - Returns plain embed with hearbeat and latency in ms.
   - Credit to [ComfortablyCoding](https://github.com/ComfortablyCoding)
2. **cogs**:
   - Easy way to load, unload and reload cogs. 
   - Has `commands.is_owner` check


## [menus](https://github.com/chrisdewa/dpytools/blob/master/dpytools/menus.py) (reaction menus) 
### `from dpytools.menus import ...`
1. **arrows**:
   - Takes a list of `discord.Embed` objects and displays it with a navigation menu.
   - Features:
      - pause (remove reactions keep embed)
      - next, previous, first, last
      - close button.
2. **confirm**:
   - Takes a `discord.Message` and adds reactions to confirm or cancel.
   - If reaction is 👍 returns `True`
   - If reaction is ❌ returns `False`
   - If timeout is reached returns `None`
3. **multichoice**:
   - Takes a list of strings for the user to select one from using reactions
   - Simple example:
      ```python
      @bot.command()
      async def test(ctx):
         options = [str(uuid4()) + '\n\n' for _ in range(110)]
         choice = await multichoice(ctx, options)
         await ctx.send(f'You selected: {choice}')
      ```
      ![multichoice](https://user-images.githubusercontent.com/62080903/118138429-ed8b6280-b3cb-11eb-9f06-415b8cb22822.gif)



## [parsers](https://github.com/chrisdewa/dpytools/blob/master/dpytools/parsers.py) (discord.ext.commands.command argument converters) 
### `from dpytools import ...`
1. **to_spongebob_case**:
   - Takes a string argument and returns it with alternating caps
   - Input:`'Have a nice day'`, Output: `'hAvE A NiCe dAy'`
2. **to_upper**:
   - Takes a string argument and returns it in caps
   - Input:`'Have a nice day'`, Output: `'HAVE A NICE DAY'`
2. **to_lower**:
   - Takes a string argument and returns it in lower case
   - Input:`'HAVE A NICE DAY'`, Output: `'have a nice day'`
3. **to_timedelta**:
   - Takes a string in the format `<number>[s|m|h|d]` and returns its equivalent timedelta object
   - Input: `'2h30m'`, Output: `timedelta(hours=2, minutes=30)`
4. **Trimmer**:
   - Callable class. Constructor takes a `max_lenght` (int) parameter.
      The instance takes a string arguments and trims it to `max_lenght` if the string was longer than that
      an `end_sequence` (default `'...'`) is attached at the end removing that many additional characters.
      - `trimmer = Trimmer(50)` 
      - Input: `'this is a very long and boring text that should be trimmed for whatever reason'`
      - Output: `'this is a very long and boring text that should...'`
5. **to_month**:
   - Returns the passed month as integer.
   - input argument can be complete name of the month ('january'), short ('jan') or number ('01'/'1')
   - Case insensitive
6. **MemberUserProxy**:
   - Tries to convert argument to a Member object, then to User and finally to a snowflake-like object assuming the
     argument was an int.
   - Useful for bans and database lookups.


## [waiters](https://github.com/chrisdewa/dpytools/blob/master/dpytools/waiters.py)
### `from dpytools.waiters import ...`
1. **wait_for_regex**:
   - Waits for and returns a message that contains a match for the specified pattern
2. **wait_for_author**:
   - Returns a single message from ctx.author in ctx.channel, features a 'cancel' sequence


## [embeds](https://github.com/chrisdewa/dpytools/blob/master/dpytools/embeds.py) 
### `from dpytools.embeds import ...`
1. **paginate_to_embeds**:
   - Takes a long string and returns a list of embeds paginating the string.
   - Sets the footer to `{page_number}/{total_pages}`
2. **dict_to_fields**:
   - Takes a dictionary where each pair of key/value sets acordingly the name and value of a field in the passed embed.
   - Credit to [fuyu78](https://github.com/fuyu78)
3. **Embed**:
   - Modification of the base `discord.Embed` class that has some added functionality.
   - Additions to the main class:
      - The constructor accepts image and thumbnail.
      - Custom method `add_fields` that accepts kwargs and takes each key/value pair as the name and value 
        parameter of each field.
      - example:
          ```python
          embed = Embed(
              title="The title",  
              description="the description",
              color=0x00FFFF,
              image="https://live.staticflickr.com/4520/37911599015_17f305061d_b.jpg",
              thumbnail="https://cdn.discordapp.com/avatars/365957462333063170/21bc9c9032b373f88db88723c5d5a9ee.webp",
              timestamp=datetime.utcnow(),
          )
          embed.add_fields(inline=False, first='first field', second='second field')
          ```
4. **PaginatedEmbeds**:
   - The class takes a base embed and a dictionary with any amount of fields and returns a list
   of embeds with the maximum amount of fields by field number AND maximum embed character limit.
   - Credit to [Kshitiz-Arya](https://github.com/Kshitiz-Arya)


More to come...



