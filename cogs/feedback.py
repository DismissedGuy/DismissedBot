from discord.ext import commands
import discord

class Feedback():
	def __init__(self, bot):
		self.client = bot
		
	async def on_message(message):
		if message.author == self.client.user or not message.channel.name == None or message.content.startswith('::'):
			return
		
		await self.client.say("You want to send this feedback to the owner:\n```{}```\nIs this correct? (Yes/No)".format(message.content))
		
		confirm = await self.client.wait_for_message(timeout=60.0, channel=message.author)
		
		if confirm == None or not confirm.content.lower() in ["yes", "y", "yea", "yep", "ye"]:
			self.client.say(":x: Feedback discarded.")
			return
		
		embed = discord.Embed(color=0xFF000)
		embed.add_field(name="{0.name}#{0.discriminator} (ID: {0.id})" , value=message.content, inline=False)
		embed.set_footer(text=confirm.timestamp)
		
		await self.client.send_message(self.client.get_channel("408972669615341568"), ":exclamation: Received a new feedback!", embed=embed)
		await self.client.say(":white_check_mark: Successfully sent feedback!")