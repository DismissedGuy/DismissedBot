import discord
import inspect
import ctypes #opus shit ugh
import subprocess
from discord.ext import commands

class Owner():
	def __init__(self, bot):
		self.client = bot
		owner = '311869975579066371'
		
	@commands.command()
	async def bash(self, *, command: str):
		if not ctx.message.author.id == self.owner:
			return
		try:
			output = subprocess.run(command.split(), stdout=subprocess.PIPE)
			if not output == "" or output == " ": #empty
				await self.client.say("```" + output.stdout.decode('utf-8') + "```")
			else:
				await self.client.say("(No output)")
		except Exception as error:
			await self.client.say("```" + error.stdout.decode('utf-8') + "```")

	@commands.command(pass_context=True, hidden=True)
	async def debug(self, ctx, *, code: str):
		if not ctx.message.author.id == self.owner:
			return
		code = code.strip('` ')
		python = '```py\n{}\n```'
		result = None

		env = {
			'bot': self.client,
			'ctx': ctx,
			'message': ctx.message,
			'server': ctx.message.server,
			'channel': ctx.message.channel,
			'author': ctx.message.author
		}

		env.update(globals())

		try:
			result = eval(code, env)
			if inspect.isawaitable(result):
				result = await result
		except Exception as e:
			await self.client.say(python.format(type(e).__name__ + ': ' + str(e)))
			return

		await self.client.say(python.format(result))

	@commands.command(pass_context=True, hidden=True)
	async def announcement(self, ctx, *, announcement=None):
		if not ctx.message.author.id == self.owner or announcement == None:
			return
		embed=discord.Embed(title="ðŸ“£ New announcement!", description=announcement, color=0xff00ff)
		embed.set_footer(text=ctx.message.timestamp)
		for botserver in client.servers:
			try:
				msgchannel = discord.utils.get(botserver.channels, name='general')
			except:
				pass
			await self.client.send_message(msgchannel, embed=embed)
    
	@commands.command(pass_context=True, hidden=True)
	async def presence(self, ctx, *, game=None):
		if not ctx.message.author.id == self.owner:
			return
		await self.client.change_presence(game=discord.Game(name=game, type=0))
		if game == None:
			await self.client.say("Removed the current playing status!")
		else:
			await self.client.say('Changed playing status to "{}"!'.format(game))
			

def setup(bot):
	client.add_cog(Owner(bot))