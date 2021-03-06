from discord.ext import commands
import discord
import os, pytz, datetime, asyncio
import difflib
from geopy.distance import vincenty

class Utilities():

    def __init__(self, bot):
        self.client = bot

    @commands.command(description='Fetch the avatar of a user')
    async def avatar(self, ctx, user : discord.User):
        embed = discord.Embed(title=user.avatar_url, color=16648720)
        embed.set_image(url=user.avatar_url)

        await ctx.send(":white_check_mark: Here's the avatar for `{}`!".format(str(user)), embed=embed)

    @commands.command(description='Check dbans for a user ID')
    async def dbans(self, ctx, user : discord.User):
        payload = {
            'token': self.client.config['DBANS_TOKEN'],
            'userid': user.id,
            'version': 3,
        }
        async with self.client.aiosession as cs:
            async with cs.post('https://bans.discordlist.net/api', data=payload) as resp:
                r = resp

        #very dirty I know
        if r.text == 'False':
            'not in DBans'
            listed = False
            color = 54528
        else:
            'in DBans'
            data = await r.json()
            listed = True
            rid = data[0]
            reason = data[3]
            proof = data[4][9:(- 11)]
            color = 16648720

        embed = discord.Embed(color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='User:', value='{0} (ID: {0.id})'.format(user), inline=False)
        embed.add_field(name='Is on DBans:', value=listed, inline=False)

        if listed:
            embed.add_field(name='Report ID:', value=rid, inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.add_field(name='Proof:', value=proof, inline=True)

        await ctx.send(':white_check_mark: DBans list fetched!', embed=embed)

    @commands.command(description='Shows the current time.')
    async def time(self, ctx, *, tz='Europe/London'):
        if tz.lower() == 'list':
            with open('timezones.txt', 'w+') as timezones:
                timezones.write(str(pytz.all_timezones))
            await ctx.channel.send(file=discord.File('tz.txt', filename='tz.txt'))
            os.remove('tz.txt')
            return

        if (not (tz in pytz.all_timezones)):
            await ctx.send(':x: Invalid timezone specified! For a list of all timezones, do `::time list`.')
            return

        currmsg = await ctx.send("Please wait while I'm getting the time...")
        confirm = 'Time for `{}`:'.format(tz)

        for i in range(7):
            await asyncio.sleep(10)
            now = datetime.datetime.now(pytz.timezone(tz))
            date = ':calendar: {0.day}-{0.month}-{0.year}'.format(now)
            time = ':clock: {0.hour}:{0.minute}:{0.second}'.format(now)

            embed = discord.Embed(color=16711680)
            embed.add_field(name=date, value=time, inline=False)
            embed.set_footer(text='All info provided by my system time.')

            await currmsg.edit(new_content=confirm, embed=embed, content=confirm)

def setup(bot):
    bot.add_cog(Utilities(bot))
