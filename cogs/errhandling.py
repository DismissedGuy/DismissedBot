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
            errormsg = f':x: You\'re missing one or more arguments! Check `::help {ctx.command.qualified_name}` for the correct format.'

        #finishing user output
        options = ['📰', '📧']

        errormsg += """
        ------------------------------------------------------------------------
        :newspaper: - Show traceback (for debugging purposes)
        :e_mail: - Send as a bug report (if you think this is an error)
        """

        msg = await ctx.send(errormsg)
        for emote in options.:
            await msg.add_reaction(emote)

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reac, usr: str(reac.emoji) in options and reac.message.id == msg.id and not usr.bot)
        except asyncio.TimeoutError:
            return

        if str(reaction) == '📰':
            await msg.edit(content=msg.content, embed=discord.Embed(description=f"```{''.join(format_list(extract_tb(error.__traceback__)))}\n{error}```", color=0xFF0000))
        elif str(reaction) == '📧':
            await self.client.get_guild(340929662131765259).get_channel(423156782743945226).send(':bug: Traceback coming soon:tm:)
            await ctx.send(":white_check_mark: Successfully reported this error as a bug!")

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
