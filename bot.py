import os
import logging
from geopy.distance import vincenty
import subprocess
from discord.ext.commands import Bot
import discord

logging.basicConfig(level=logging.INFO) #set up logging to Heroku terminal

client = Bot(description="A Dismissed Bot", command_prefix="::", pm_help = True)

@client.command()
async def version():
    bot.say(discord.__version__ + "\n" + discord.version_info)

@client.command()
async def bash(*, command: str):
    try:
        output = subprocess.run(command.split(), stdout=subprocess.PIPE, shell=True)
        if not output == "": #empty
            await bot.say("```" + output.stdout.decode('utf-8') + "```")
        else:
            await bot.say("(No output)")
    except Exception as error:
        await bot.say("```" + error.stdout.decode('utf-8') + "```")

@client.command()
async def dist(place1x, place1y, place2x, place2y):
    place1 = (place1x, place1y)
    place2 = (place2x, place1y)
    distance = vincenty(place1, place2).miles

    await client.say(str(distance) + " miles")

@client.event
async def on_ready():
    print('------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------------------')

client.run(os.environ['BOT_TOKEN'])
