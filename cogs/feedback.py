from discord.ext import commands
import discord

class Feedback():
	def __init__(self, bot):
		self.client = bot
		
	async def on_message(self, message):
		if message.author == self.client.user or not message.channel.name == None or message.content.startswith('::'):
			print("go return")
			return
		
		await self.client.send_message(message.author, "You want to send this feedback to the owner:\n```{}```\nIs this correct? (Yes/No)".format(message.content))
		
		confirm = await self.client.wait_for_message(timeout=60.0, author=message.author, channel=None)
		
		if confirm == None or not confirm.content.lower() in ["yes", "y", "yea", "yep", "ye"]:
			await self.client.send_message(message.author, ":x: Feedback discarded.")
			return
		
		embed = discord.Embed(color=0xFF000)
		embed.add_field(name="{0.name}#{0.discriminator} (ID: {0.id})" , value=message.content, inline=False)
		embed.set_footer(text=confirm.timestamp)
		
		await self.client.send_message(self.client.get_channel("408972669615341568"), ":exclamation: Received a new feedback!", embed=embed)
		await self.client.send_message(message.author, ":white_check_mark: Successfully sent feedback!")
		
def setup(bot):
	bot.add_cog(Feedback(bot))