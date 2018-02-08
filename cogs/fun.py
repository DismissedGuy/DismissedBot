from geopy.distance import vincenty
from cleverwrap import CleverWrap
import os, requests
from discord.ext import commands
import discord

class Fun():

    def __init__(self, bot):
        self.client = bot

    async def on_message(self, message):
        if (message.author == self.client.user) or (message.channel.name == None) or message.content.startswith('::'):
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
        predicts = requests.get('http://suggestqueries.google.com/complete/search?client=firefox&q=' + query)
        if (not (predicts.status_code == 200)):
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

def setup(bot):
    bot.add_cog(Fun(bot))