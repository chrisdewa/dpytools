


# How to add a command to my bot?
```python
from dpytools.commands import latency
bot.add_command(latency)
```

# How to add a command to a specific cog?
```python
@commands.command()
async def new_command(ctx):
    await ctx.send('it works')

cog = bot.get_cog("CogName") # Gets the cog instance
cog.__cog_commands__ += (new_command,) # Updates the __cog_commands__, this is to show up in HelpCommand
new_command.cog = cog # Set the cog attribute with your instance, this is to make the library pass self
bot.add_command(new_command) # Adds the command to the bot
```
_Taken from R. Danny_

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
Consider the prefix to be "`!`". 

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
[!example](https://imgur.com/a/aJkO9h3)














