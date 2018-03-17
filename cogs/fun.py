from geopy.distance import vincenty
from cleverwrap import CleverWrap
import os, random
from discord.ext import commands
import discord

class Fun():

    def __init__(self, bot):
        self.client = bot

    async def on_message(self, message):
        if (message.author == self.client.user) or (isinstance(message.channel, discord.abc.PrivateChannel)) or message.content.startswith('::'):
            return
        if message.channel.name.lower() == 'cleverbot':
            cw = CleverWrap(os.environ['CLEVER_TOKEN'])
            if message.content.lower() == 'reset':
                cw.reset()
                await message.channel.send(':white_check_mark: Successfully reset cleverbot configuration!')
            else:
                await message.channel.trigger_typing()
                await message.channel.send(cw.say(message.content))
            await self.client.process_commands(message)

    @commands.command(description='Make google autocomplete your query!')
    async def complete(self, ctx, *, query):
        predicts = await self.client.aiohttp.get('http://suggestqueries.google.com/complete/search?client=firefox&q=' + query)
        if not predicts.status == 200:
            await ctx.send(':warning: An error occured while retrieving the data! Please try again later.')
            return
        predicts = predicts.text[len(query) + 5:len(predicts.text) - 2].replace('"', '').split(',')

        if predicts == ['']:
            await ctx.send(":x: I couldn't find any autocompletions!")
            return

        elif len(predicts) > 5:
            predicts = predicts[0:5]

        embed = discord.Embed(color=16711680)
        embed.add_field(name='A total of {} results were returned:'.format(len(predicts)), value='\n'.join(predicts))
        await ctx.channel.send(':white_check_mark: Successfully retrieved autocompletions!', embed=embed)

    @commands.command(descrption="Choose from 2 or more random choices!", aliases=['choice'])
    async def choose(self, ctx, *choices):
        if len(choices) <= 1: #command fails when len(args) == 0, but you can never be too sure...
            await ctx.send(":exclamation: You only gave me one thing to choose from! You don't wanna play this unfair, do you..?")
            return

        await ctx.send(f":white_check_mark: I chose: `{random.choice(choices)}`!")

def setup(bot):
    bot.add_cog(Fun(bot))
