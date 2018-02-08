import discord
import inspect
import ctypes
import subprocess
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
            'server': ctx.guild,
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def presence(self, ctx, *, game=None):
        await self.client.change_presence(game=discord.Game(name=game, type=0))
        
        if game == None:
            await ctx.send('Removed the current playing status!')
        else:
            await ctx.send('Changed playing status to "{}"!'.format(game))

def setup(bot):
    bot.add_cog(Owner(bot))