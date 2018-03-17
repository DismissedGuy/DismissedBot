import sys
import asyncio
from traceback import format_list, extract_tb
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, bot):
        self.client = bot

    async def on_command_error(self, ctx, error):
        # prevent commands with local handlers being handled here
        if hasattr(ctx.command, 'on_error'):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, commands.errors.MissingRequiredArgument):
            msg = await ctx.send(f':x: You\'re missing one or more arguments! Check `::help {ctx.command.qualified_name}` for the correct format.')
            options = ['📧']
        elif isinstance(error, commands.errors.NotOwner):
            msg = await ctx.send('Hmmm... I don\'t think you are my owner.')
            options = [] #do not allow bug reports
        else: #unhandled
            msg = await ctx.send(':x: Uh oh.. An unhandled exception has occured! Can you _please_ be so nice to leave me a bug report? Thanks!')
            options = ['📰', '📧']

        #finishing user output
        for emote in options:
            await msg.add_reaction(emote)

        already_sent = False #max. 1 bug report
        for i in range(4): #only let the user react 3 times so they won't keep the loop running for too long.
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reac, usr: str(reac.emoji) in options and reac.message.id == msg.id and not usr.bot)
            except asyncio.TimeoutError:
                return

            if str(reaction) == '📰':
                await msg.edit(content=msg.content, embed=discord.Embed(description={error}, color=0xFF0000))
            elif str(reaction) == '📧':
                if already_sent:
                    await ctx.send(":x: You've already sent a bug report for this error!")
                else:
                    report = f"""
:bug: Report by {ctx.author} regarding the command {ctx.command.qualified_name}:
    **Traceback:**
```{''.join(format_list(extract_tb(error.__traceback__)))}```
    **Error:**
```{error}```
"""
                    await self.client.get_guild(340929662131765259).get_channel(423156782743945226).send(report)
                    await ctx.send(":white_check_mark: Successfully reported this error as a bug!")

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
