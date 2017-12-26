import os
import logging
from geopy.distance import vincenty
import discord

logging.basicConfig() #set up logging to Heroku terminal

client = Bot(description="A Dismissed Bot", command_prefix="::", pm_help = True)

@client.command
async def dist(ctx, place1x, place1y, place2x, place2y):
    place1 = (place1x, place1y)
    place2 = (place2x, place1y)
    try:
        client.say(vincenty(newport_ri, cleveland_oh).miles)
    except:
        client.say("You sure you did it correctly?")

@client.event
async def on_ready():
    print('------------------')
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------------------')

client.run(os.environ['BOT_TOKEN'])
