# Libraries i may or may not use
from utils.util import clean_code
import discord
from discord.ext import commands
import logging
from pathlib import Path
import json
import random
import platform
import io
import contextlib
import textwrap
import traceback
import requests
from num2words import num2words
from PIL import Image, ImageColor

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Defines some stuff idk
secrets_file = json.load(open(cwd + "/secrets.json"))
command_prefix = "b:"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.config_token = secrets_file["token"]
logging.basicConfig(level=logging.INFO)

# Are yah ready kids?
@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nCurrent prefix: '{command_prefix}'"
    )

    await bot.change_presence(activity=discord.Game(name="Undergoing Renovations"))


# Errors are not pog
@bot.event
async def on_command_error(ctx, error):
    ignored_errors = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored_errors):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Stop it. Get some perms.", mention_author=False)


# Command center
@bot.command(name="test")
async def test(ctx):
    """
    A simple test command
    """
    test_grades = ["an A", "a B", "a C", "a D", "an F"]

    await ctx.send(f"{ctx.author.mention} got {random.choice(test_grades)}")


@bot.command(name="info")
async def info(ctx):
    """
    Gives info about Botnobi
    """
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(bot.guilds)
    user_count = len(set(bot.get_all_members()))

    embed = discord.Embed(
        title=f":information_source: Botnobi",
        description="\uFEFF",
        color=ctx.guild.me.color,
        timestamp=ctx.message.created_at,
    )

    embed.add_field(
        name="<:github:842921746277203978>",
        value="[Repo](https://github.com/MysticalApple/Botnobi-2.0)",
    )
    embed.add_field(name="Python Version", value=python_version)
    embed.add_field(name="Discord.py Version", value=dpy_version)
    embed.add_field(name="Servers", value=server_count)
    embed.add_field(name="Users", value=user_count)
    embed.add_field(name="Bot Creator", value="<@!595719716560175149>")

    embed.set_footer(text=f"As of")
    embed.set_author(name=ctx.guild.me.display_name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="disconnect")
@commands.is_owner()
async def disconnect(ctx):
    """
    Takes Botnobi offline
    """
    await ctx.send("Disconnecting...")
    await bot.logout()


@bot.command(name="eval")
@commands.is_owner()
async def eval(ctx, *, code):
    code = clean_code(code)

    local_variables = {"discord": discord, "commands": commands, "bot": bot, "ctx": ctx}

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(f"async def func():\n{textwrap.indent(code, '    ')}", local_variables)

            obj = await local_variables["func"]()
            result = f"py\n‌{stdout.getvalue()}\n"

    except Exception as e:
        result = "".join(traceback.format_exception(e, e, e.__traceback__))

    await ctx.send(f"```{result}```")


@bot.command(name="sheep")
async def sheep(ctx):
    await ctx.send(
        "<a:seansheep:718186115294691482>```\n         ,ww\n   wWWWWWWW_)\n   `WWWWWW'\n    II  II```"
    )


@bot.command(name="emotize")
async def emotize(ctx, *, message):
    output = ''
    
    for l in message:
        if l == ' ':
            output += l
        elif l == '\n':
            output += l
        elif l.isdigit():
            numword = num2words(l)
            output += f':{numword}:'
        elif l.isalpha():
            l = l.lower()
            output += f':regional_indicator_{l}:'
    
    await ctx.send(output)


@bot.command(name="inspire")
async def inspire(ctx):
    r = requests.get('https://inspirobot.me/api?generate=true')
    await ctx.send(r.text)


#@bot.command(name="pfp")
#async def pfp(ctx, *, requested_user):
#boring to implement, might do soon


@bot.command(name="color")
async def color(ctx, *, hex):
    try:
        color = ImageColor.getrgb(hex)
    
    except:
        await ctx.reply("Valid color codes can be found here: https://pillow.readthedocs.io/en/stable/reference/ImageColor.html?highlight=getrgb#PIL.ImageColor.getrgb", mention_author=False)

    img = Image.new('RGBA', (480, 480), color = color)
    img.save('color.png')
    await ctx.send(file = discord.File('color.png'))    

# Run the damn thing already
bot.run(bot.config_token)
