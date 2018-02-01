from discord.ext import commands
import discord
import datetime
import asyncio
from geopy.distance import vincenty

class Utilities():
	def __init__(self, bot):
		self.client = bot
	
	@commands.command()
	async def dist(self, long1, lat1, long2, lat2):
		place1 = (long1, lat2)
		place2 = (long2, lat2)
		distance = vincenty(place1, place2).miles

		await self.client.say(str(distance) + " miles")
	
	@commands.command(pass_context=True, description='Shows the current time.')
	async def time(self, *tz):
		if not tz:
			print("not specified")
			await self.client.say(":x: You didn't specify your timezone! Please tell me yours (in GMT).")
			tz = await self.client.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
		try:
			tz = int(tz.replace("GMT",""))
		except:
			print("int parsing failed")
			error = True
		if error or not tz in range(-12,15):
			await self.client.say(":x: `{}` is not a valid timezone!".format(tz))
			return
		
		currmsg = await self.client.say("Please wait while I'm getting the time...")
		
		confirm = "Here's the time for your timezone!"
		
		for i in range(13): #update 12 times (1 min)
			await asyncio.sleep(5)
			
			#update time
			now = datetime.datetime.now()
			date = "{0.day}-{0.month}-{0.year}".format(now)
			time = "{0.hour}:{0.minute}:{0.second}".format(now)
			
			#create embed
			embed=discord.Embed()
			embed.add_field(name=date, value=time, inline=False)
			embed.set_footer(text="All info provided by my system time.")
			
			#updating the message
			await self.client.edit_message(currmsg, new_content=confirm, embed=embed)

def setup(bot):
	bot.add_cog(Utilities(bot))