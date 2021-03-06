from discord.ext import commands
import discord

class About():
    def __init__(self, bot):
        self.client = bot

    @commands.command(description='Shows the API latency')
    async def ping(self, ctx):
        await ctx.send(":ping_pong: Pong! Latency: `{}ms`".format(round(self.client.latency * 1000)))

def setup(bot):
    bot.add_cog(About(bot))
