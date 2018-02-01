from geopy.distance import vincenty
from cleverwrap import CleverWrap
import os
from discord.ext import commands
import discord

class Fun():
	def __init__(self, bot):
		self.client = bot
		
	async def on_message(self, message):
		if message.author == self.client.user or message.startswith('::'):
			return

		if message.channel.name.lower() == 'cleverbot':
			cw = CleverWrap(os.environ['CLEVER_TOKEN'])
			if message.content.lower() == 'reset':
				cw.reset()
				await self.client.send_message(message.channel, "Successfully reset cleverbot configuration!")
			else:
				await self.client.send_typing(message.channel)
				await self.client.send_message(message.channel, cw.say(message.content))

			await self.client.process_commands(message)

def setup(bot):
	bot.add_cog(Fun(bot))