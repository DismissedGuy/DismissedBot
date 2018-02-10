from discord.ext import commands
import discord
import os, pytz, datetime, asyncio, requests
import difflib
from geopy.distance import vincenty

class Utilities():

    def __init__(self, bot):
        self.client = bot
        
    def get_member_by_name(self, ctx, search):
        names = difflib.get_close_matches(search, [z.name for z in ctx.guild.members], n=5, cutoff=0.4)
        users = []
        for i in names:
            users.append(discord.utils.find(lambda z: z.name == i, ctx.guild.members))
        
        if not users:
            await ctx.send(":x: I couldn't find any users! Tip: try an ID as input.")
            return False #error occured
        elif len(users) > 1:
            await ctx.send(":exclamation: Multiple users were found:\n" + '\n- '.join(["**"+v.name+"#"+v.discriminator+"**" for v in users]))
            return False #error occured
        else: #1 user found, return the ID of that user
            return users[0].id
        
    @commands.command(description='Fetch the avatar of a user')
    async def avatar(self, ctx, id):
        if not id.isdecimal(): #assume they're passing a search
            id = self.get_member_by_name(ctx, id)
            if not id: #returned an error
                return #handling is already done
        
        try:
            user = await self.client.get_user_info(id)
        except Exception as e:
            await ctx.send(":x: Sorry, but at the moment, only user IDs are supported! Please check your input and try again.")
            print(e)
            return
            
        embed = discord.Embed(title='Link: {}'.format(user.avatar_url), color=16648720)
        embed.set_image(url=user.avatar_url)
        
        await ctx.send(":white_check_mark: Here's the avatar for `{0.name}#{0.discriminator}`!".format(user), embed=embed)

    @commands.command(description='Check dbans for a user ID')
    async def dbans(self, ctx, id):
        if not id.isdecimal(): #assume they're passing a search
            id = self.get_member_by_name(ctx, id)
            if not id: #returned an error
                return #handling is already done
        
        try:
            user = await self.client.get_user_info(int(id))
        except:
            await ctx.send(':x: Please enter a correct user ID!')
            return
        
        payload = {
            'token': os.environ['DBANS_TOKEN'],
            'userid': id,
            'version': 3,
        }
        r = requests.post('https://bans.discordlist.net/api', data=payload)
        
        #very dirty I know
        if r.text == 'False':
            'not in DBans'
            listed = False
            color = 54528
        else:
            'in DBans'
            listed = True
            rid = r.json()[0]
            reason = r.json()[3]
            proof = r.json()[4][9:(- 11)]
            color = 16648720
        
        embed = discord.Embed(color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='User:', value='{0.name}#{0.discriminator} (ID: {0.id})'.format(user), inline=False)
        embed.add_field(name='Is on DBans:', value=listed, inline=False)

        if listed:
            embed.add_field(name='Report ID:', value=rid, inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.add_field(name='Proof:', value=proof, inline=True)
        
        await ctx.send(':white_check_mark: DBans list fetched!', embed=embed)

    @commands.command()
    async def dist(self, ctx, long1, lat1, long2, lat2):
        place1 = (long1, lat2)
        place2 = (long2, lat2)
        distance = vincenty(place1, place2).miles
        await ctx.send(str(distance) + ' miles')

    @commands.command(description='Shows the current time.')
    async def time(self, ctx, *, tz='Europe/London'):
        if tz.lower() == 'list':
            with open('tz.txt', 'w+') as timezones:
                timezones.write(str(pytz.all_timezones))
            await ctx.channel.send(file=discord.File('tz.txt', filename='tz.txt'))
            os.remove('tz.txt')
            return
        
        if (not (tz in pytz.all_timezones)):
            await ctx.send(':x: Invalid timezone specified! For a list of all timezones, do `::time list`.')
            return
        
        currmsg = await ctx.send("Please wait while I'm getting the time...")
        confirm = 'Time for `{}`:'.format(tz)
        
        for i in range(21):
            await asyncio.sleep(3)
            now = datetime.datetime.now(pytz.timezone(tz))
            date = ':calendar: {0.day}-{0.month}-{0.year}'.format(now)
            time = ':clock: {0.hour}:{0.minute}:{0.second}'.format(now)
            
            embed = discord.Embed(color=16711680)
            embed.add_field(name=date, value=time, inline=False)
            embed.set_footer(text='All info provided by my system time.')
            
            await currmsg.edit(new_content=confirm, embed=embed, content=confirm)

def setup(bot):
    bot.add_cog(Utilities(bot))