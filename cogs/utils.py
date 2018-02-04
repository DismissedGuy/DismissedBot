from discord.ext import commands
import discord
import os, pytz, datetime, asyncio, requests
from geopy.distance import vincenty

class Utilities():
	def __init__(self, bot):
		self.client = bot
		
	@commands.command(pass_context=True, description="Check dbans for a user ID")
	async def dbans(self, ctx, id="390709163837095937"):
		try:
			user = await self.client.get_user_info(id)
		except discord.NotFound, discord.HTTPException :
			await self.client.say(":x: Please enter a correct user ID!")
			return
		
		payload = {"token":os.environ['DBANS_TOKEN'], "userid":id, "version":3}
		r = requests.post("https://bans.discordlist.net/api", data=payload)
		
		#I KNOW the following is dirty af but hey it works ok so yea
		if r.text == 'False':
			"""not in DBans"""
			embed=discord.Embed(color=0x00d500)
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="User:", value="{0.name}#{0.discriminator} (ID: {0.id})".format(user), inline=False)
			embed.add_field(name="Is on DBans:", value=False, inline=False)
		else:
			"""in DBans"""
			reason = r.json()[3]
			proof = r.json()[4][9:-11]
			
			embed=discord.Embed(color=0xfe0a10)
			embed.set_thumbnail(url=user.avatar_url)
			embed.add_field(name="User:", value="{0.name}#{0.discriminator} (ID: {0.id})".format(user), inline=False)
			embed.add_field(name="Is on DBans:", value=True, inline=False)
			embed.add_field(name="Reason:", value=reason, inline=True)
			embed.add_field(name="Proof:", value=proof, inline=True)
			
		await self.client.send_message(ctx.message.channel, ":white_check_mark: DBans list fetched!", embed=embed)
	
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
			await self.client.send_file(ctx.message.channel, 'tz.txt')
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