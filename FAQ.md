
# How do I use Color enum class?
```python
from dpytools import Color

@bot.command(name='color-test')
async def color_test(ctx):
    # Use the color class to access the color you need by getting its value
    fire_orange = Color.FIRE_ORANGE.value
    await ctx.send(embed=discord.Embed(description="This is fire orange color",
                                       color=fire_orange))
    # Or just use the class to set the embed color
    await ctx.send(embed=discord.Embed(description="This is cyan",
                                       color=Color.CYAN))
```

# How do I use the Emoji enum class?
Example using reactions
```python
from dpytools import Emoji
@bot.listen('on_raw_reaction_add')
async def reaction_listener(payload):
    if payload.user_id == bot.user.id: 
        return
    
    if payload.emoji.name in [Emoji.HEART, Emoji.FIRE, Emoji.GREEN_CHECK]:
        ch = bot.get_channel(payload.channel_id)
        await ch.send('I love those emojis!')
```
This listener will wait for an appropiate reaction and send a message to the channel where it happened.

# How to add a command to my bot?
```python
from dpytools.commands import latency
bot.add_command(latency)
```

# How to add a command to a specific cog?
```python
from dpytools.commands import cogs

cog = bot.get_cog("MyCog") # Gets the cog instance
cog.__cog_commands__ += (cogs,) # Updates the __cog_commands__, this is to show up in HelpCommand
cogs.cog = cog # Set the cog attribute with your instance, this is to make the library pass self
bot.add_command(cog) # Adds the command to the bot
```

# How to use parsers?
```python
from dpytools.parsers import to_timedelta

# add the parser as a typehint to a command argument
@bot.command()
async def test(ctx, time: to_timedelta):
    await ctx.send(time)
```
to_timedelta takes a string in the format "<number>[s|m|h|d]" and turns it into a timedelta object.
The user will call the command like this: `!test 2h30m`
Time parameter will then be `timedelta(hours=2, minutes=30)`

# How to use checks?
```python
from dpytools.checks import admin_or_roles

@bot.command()
@admin_or_roles('Mods', 1234567890, 'Staff')
async def test(ctx):
    await ctx.send('it works')
```
The check will pass only if `ctx.author` has admin permissions in the guild **OR** has any listed roles.

# How to use menus?
```python
from dpytools.menus import confirm
@bot.command()
async def test(ctx):
    msg = await ctx.send('Please confirm to this important message')
    confirmation = await confirm(ctx, msg)
    if confirmation:
        await msg.edit(content='Confirmed')
    elif confirmation is False:
        await msg.edit(content='Cancelled')
    else:
        await msg.edit(content='Timeout')
```
![confirm-example](https://user-images.githubusercontent.com/62080903/116580087-a89a0300-a8d8-11eb-8916-d19a0bf0853f.gif)















