import os
import inspect
import logging
from geopy.distance import vincenty
import subprocess
from discord.ext.commands import Bot
import discord

logging.basicConfig(level=logging.INFO) #set up logging to Heroku terminal

owner = '311869975579066371'
client = Bot(description="A Dismissed Bot", command_prefix="::", pm_help = True)
Server = discord.Server

@client.command()
async def version():
    bot.say(discord.__version__ + "\n" + discord.version_info)

@client.command()
async def bash(*, command: str):
    if not ctx.message.author.id == owner:
      return
    try:
        output = subprocess.run(command.split(), stdout=subprocess.PIPE)
        if not output == "" or output == " ": #empty
            await client.say("```" + output.stdout.decode('utf-8') + "```")
        else:
            await client.say("(No output)")
    except Exception as error:
        await client.say("```" + error.stdout.decode('utf-8') + "```")

@client.command(pass_context=True, hidden=True)
async def debug(ctx, *, code: str):
    if not ctx.message.author.id == owner:
      return
    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    env = {
        'bot': client,
        'ctx': ctx,
        'message': ctx.message,
        'server': ctx.message.server,
        'channel': ctx.message.channel,
        'author': ctx.message.author
    }

    env.update(globals())

    try:
        result = eval(code, env)
        if inspect.isawaitable(result):
            result = await result
    except Exception as e:
        await client.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    await client.say(python.format(result))

@client.command(pass_context=True, hidden=True)
async def announcement(ctx, *, announcement=None):
    if not ctx.message.author.id == owner or announcement == None:
        return
    embed=discord.Embed(title="📣 New announcement!", description=announcement, color=0xff00ff)
    embed.set_image(client.user.avatar_url)
    async for botserver in client.servers:
        await client.send_message(client.get_channel(discord.utils.find(lambda c: c.name == 'general', botserver.channels).id), embed=embed)
    
@client.command(pass_context=True, hidden=True)
async def presence(ctx, *, game=None):
    if not ctx.message.author.id == owner:
        return
    await client.change_presence(game=discord.Game(name=game, type=0))
    if game == None:
        await client.say("Removed the current playing status!")
    else:
        await client.say('Changed playing status to "{}"!'.format(game))

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
