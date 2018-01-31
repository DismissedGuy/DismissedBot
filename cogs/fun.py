from geopy.distance import vincenty
from cleverwrap import CleverWrap
import os
from discord.ext import commands
import discord

class Fun():
	def __init__(self, bot):
		self.client = bot
		
	async def on_message(self, message):
		if message.author == self.client.user:
			return

		if message.channel.name.lower() == 'cleverbot':
			cw = CleverWrap(os.environ['CLEVER_TOKEN'])
			if message.content.lower() == 'reset':
				cw.reset()
				await self.client.send_message(message.channel, "Successfully reset cleverbot configuration!")
			else:
				await client.send_typing(message.channel)
				await self.client.send_message(message.channel, cw.say(message.content))

		await self.client.process_commands(message)
	
	@commands.command()
	async def dist(self, place1x, place1y, place2x, place2y):
		place1 = (place1x, place1y)
		place2 = (place2x, place1y)
		distance = vincenty(place1, place2).miles

		await self.client.say(str(distance) + " miles")

def setup(bot):
	bot.add_cog(Fun(bot))