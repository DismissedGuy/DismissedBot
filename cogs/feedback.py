from discord.ext import commands
import asyncio
import discord

class Feedback():

    def __init__(self, bot):
        self.client = bot
        self.sending = False

    @commands.command(description='Leave my owner a feedback!')
    async def feedback(self, ctx):
        await ctx.message.add_reaction('✅')
        await asyncio.sleep(0.3)
        await ctx.author.send('Send your feedback here!')

    async def on_message(self, message):
        if (message.author == self.client.user) or (not (message.channel.name == None)) or message.content.startswith('::') or self.sending:
            return
        self.sending = True
        await message.author.send('You want to send this feedback to the owner:\n```{}```\nIs this correct? (Yes/No)'.format(message.content))
        
        def usercheck(m):
            return m.author == message.author and m.channel == message.channel
        try:
            confirm = await self.client.wait_for('message', check=usercheck, timeout=60.0)
        except asyncio.TimeoutError:
            confirm == None
        
        if (confirm == None) or (not (confirm.content.lower() in ['yes', 'y', 'yea', 'yep', 'yup', 'ye', 'sure', 'yee', 'yeah', 'yos', 'yahs', 'yesh', 'ok', 'aye aye', 'aight', 'definitely', 'arr', 'yarr'])):
            await message.author.send(':x: Feedback discarded.')
            self.sending = False
            return
        
        embed = discord.Embed(color=1044480)
        embed.add_field(name='{0.name}#{0.discriminator} (ID: {0.id})'.format(message.author), value=message.content, inline=False)
        embed.set_footer(text=confirm.timestamp)
        
        await self.client.get_channel(408972669615341568).send(':exclamation: Received a new feedback!', embed=embed)
        await message.author.send(':white_check_mark: Successfully sent feedback!')
        self.sending = False

def setup(bot):
    bot.add_cog(Feedback(bot))