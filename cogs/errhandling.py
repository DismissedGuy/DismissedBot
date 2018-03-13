import sys
import asyncio
from traceback import format_list, extract_tb
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, bot):
        self.client = bot

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
            await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reac, usr: str(reac.emoji) == '📰' and reac.message.id == msg.id and not usr.bot)
        except asyncio.TimeoutError:
            return
        await msg.edit(content=msg.content, embed=discord.Embed(description=f"```{''.join(format_list(extract_tb(error.__traceback__)))}\n{error}```", color=0xFF0000))

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
