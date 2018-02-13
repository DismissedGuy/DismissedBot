import discord
import inspect
import io
import subprocess
import traceback
from contextlib import redirect_stdout
from discord.ext import commands

class Owner():

    def __init__(self, bot):
        self.client = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bash(self, ctx, *, command: str):
        try:
            output = subprocess.run(command.split(), stdout=subprocess.PIPE)
            if (not (output == '')) or (output == ' '):
                await ctx.send(('```' + output.stdout.decode('utf-8')) + '```')
            else:
                await ctx.send('(No output)')
        except Exception as error:
            await ctx.send(('```' + error.stdout.decode('utf-8')) + '```')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def debug(self, ctx, *, code: str):
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        
        env = {
            'client': self.client,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            }
        env.update(globals())
        
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format((type(e).__name__ + ': ') + str(e)))
            return
        
        await ctx.send(python.format(result))

    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'client': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def announcement(self, ctx, *, announcement=None):
        if announcement == None:
            return
        embed = discord.Embed(title='ðŸ“£ New announcement!', description=announcement, color=16711935)
        embed.set_footer(text=ctx.message.timestamp)
        for botguild in self.client.guilds:
            try:
                msgchannel = discord.utils.get(botguild.channels, name='general')
            except:
                pass
            await msgchannel.send(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))