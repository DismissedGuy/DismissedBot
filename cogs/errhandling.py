import sys
import asyncio
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        errormsg = ':x: An unhandled exception has occured! Please try again later.'

        # This prevents any commands with local handlers being handled here
        if hasattr(ctx.command, 'on_error'):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, commands.errors.MissingRequiredArgument):
            errormsg = ':x: You\'re missing one or more arguments! Check ::help for the correct format.'

        #finishing user output
        msg = await ctx.send(errormsg)
        await msg.add_reaction('📰')

        try:
            await client.wait_for('reaction_add', timeout=60.0, check=lambda reac, _: str(reac.emoji) == '📰')
        except asyncio.TimeoutError:
            return
        await msg.edit(content=msg.content, embed=discord.Embed(description=type(error) + error + error.__traceback__), color=0cFF000)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
