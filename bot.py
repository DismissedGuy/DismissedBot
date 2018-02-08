import os
import logging
from discord.ext.commands import Bot
from discord.ext import commands
import discord

logging.basicConfig(level=logging.INFO)

'COGS (auto recognized)'
startup_extensions = ['cogs.' + cog.strip('.py') for cog in os.listdir('cogs/')]

client = Bot(description='DismissedBot is a multifunctional Discord bot focused on being very user friendly.', command_prefix='::', pm_help=True)

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension_name: str):
    'Loads an extension.'
    try:
        client.load_extension("cogs." + extension_name)
    except Exception as e:
        await ctx.send(':x: An error occured while loading the `{}` cog:\n```py\n{}: {}\n```'.format(extension_name,type(e).__name__, str(e)))
        return
    await ctx.send(':white_check_mark: Successfully loaded cog: `{}`'.format(extension_name))

@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension_name: str):
    'Unloads an extension.'
    try:
        client.load_extension("cogs." + extension_name)
    except Exception as e:
        await ctx.send(':x: An error occured while unloading the `{}` cog:\n```py\n{}: {}\n```'.format(extension_name,type(e).__name__, str(e)))
        return
    await ctx.send(':white_check_mark: Successfully unloaded cog: `{}`'.format(extension_name))

@client.event
async def on_ready():
    print(discord.__version__)
    print('------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------------------')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    client.run(os.environ['BOT_TOKEN'])
