from discord.ext import commands
import discord
import os
import pytz
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
	async def time(self, ctx, *, tz='Europe/London'):
		if tz.lower() == 'list':
			with open("tz.txt", "w+") as timezones:
				timezones.write(str(pytz.all_timezones))
				await self.client.send_file(ctx.message.channel, timezones)
			os.remove('tz.txt')
			return
		
		if not tz in pytz.all_timezones:
			await self.client.say(":x: Invalid timezone specified! For a list of all timezones, do `::time list`.")
			return
		
		currmsg = await self.client.say("Please wait while I'm getting the time...")
		
		confirm = "Time for `{}`:".format(tz)
		
		for i in range(13): #update 12 times (1 min)
			await asyncio.sleep(5)
			
			#update time
			now = datetime.datetime.now(pytz.timezone(tz))
			date = ":calendar: {0.day}-{0.month}-{0.year}".format(now)
			time = ":clock: {0.hour}:{0.minute}:{0.second}".format(now)
			
			#create embed
			embed=discord.Embed(color=0xFF0000)
			embed.add_field(name=date, value=time, inline=False)
			embed.set_footer(text="All info provided by my system time.")
			
			#updating the message
			await self.client.edit_message(currmsg, new_content=confirm, embed=embed)

def setup(bot):
	bot.add_cog(Utilities(bot))