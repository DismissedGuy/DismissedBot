import os
import logging
from discord.ext.commands import Bot
import discord

logging.basicConfig(level=logging.INFO) #set up logging to Heroku terminal

"""COGS"""
startup_extensions = ["cogs." + ext for ext in os.listdir("cogs/")]

owner = '311869975579066371'
client = Bot(description="A Dismissed Bot", command_prefix="::", pm_help = True)

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@client.event
async def on_ready():
    print('------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------------------')

if __name__ == "__main__": #load cogs
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(os.environ['BOT_TOKEN'])