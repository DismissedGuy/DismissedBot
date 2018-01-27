from geopy.distance import vincenty
from discord.ext import commands

class Fun(self, bot):
	def __init__(self, bot):
		self.client = client
	
	@client.command()
	async def dist(self, place1x, place1y, place2x, place2y):
		place1 = (place1x, place1y)
		place2 = (place2x, place1y)
		distance = vincenty(place1, place2).miles

		await self.client.say(str(distance) + " miles")

def setup(bot):
	client.add_cog(Fun(bot))