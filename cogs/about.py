from discord.ext import commands
import discord
import aiohttp

class About():
    def __init__(self, bot):
        self.client = bot
        self.bot.aiohttp = aiohttp.ClientSession() #define it here for god's sake

    @commands.command(description='Shows the API latency')
    async def ping(self, ctx):
        await ctx.send(":ping_pong: Pong! Latency: `{}ms`".format(round(self.client.latency * 1000)))

def setup(bot):
    bot.add_cog(About(bot))
