import discord
from redbot.core import commands
import random
import json
import time
import os
import datetime

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class AFK(commands.Cog):
    '''
    Class containing AFK commands/system.
    '''
    def __init__(self, bot):
        self.bot = bot
    #*
    async def update_data(self, afk, user):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = 'False'
            afk[f'{user.id}']['reason'] = 'None'
    
    async def time_formatter(self, seconds: float):
        '''
        Convert UNIX time to human readable time.
        '''
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + "d, ") if days else "") + \
            ((str(hours) + "h, ") if hours else "") + \
            ((str(minutes) + "m, ") if minutes else "") + \
            ((str(seconds) + "s, ") if seconds else "")
        return tmp[:-2]
    
    @commands.Cog.listener()
    async def on_message(self, message):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'db/afk.json')
        with open(file_path, 'r') as f:
            afk = json.load(f)
        
        for user_mention in message.mentions:
            if afk[f'{user_mention.id}']['AFK'] == 'True':
                if message.author.bot: 
                    return
                
                reason = afk[f'{user_mention.id}']['reason']
                meth = afk[f'{user_mention.id}']['time']
                embed = discord.Embed(description=f'{user_mention.mention} is AFK (<t:{meth}:R>)\n**Message:**\n{reason}', color=0xd3c1e3)
                await message.channel.send(embed=embed)
                
                meeeth = int(afk[f'{user_mention.id}']['mentions']) + 1
                afk[f'{user_mention.id}']['mentions'] = meeeth
                
                with open(file_path, 'w') as f:
                    json.dump(afk, f)
        
        if not message.author.bot:
            await self.update_data(afk, message.author)

            if afk[f'{message.author.id}']['AFK'] == 'True':

                if message.content.startswith('#'):
                    return
                
                meth = afk[f'{message.author.id}']['time']
                been_afk_for = datetime.datetime.fromtimestamp(meth, tz=None)
                mentionz = afk[f'{message.author.id}']['mentions']

                embed = discord.Embed(title=f"Welcome Back!", description=f"While you were AFK you recieved **{mentionz}** pings.", color=0xd3c1e3, timestamp=been_afk_for)
                embed.set_footer(text='AFK since')
                await message.reply(embed=embed)
                
                afk[f'{message.author.id}']['AFK'] = 'False'
                afk[f'{message.author.id}']['reason'] = 'None'
                afk[f'{message.author.id}']['time'] = '0'
                afk[f'{message.author.id}']['mentions'] = 0
                
                with open(file_path, 'w') as f:
                    json.dump(afk, f)
                
                try:
                    await message.author.edit(nick=remove(message.author.display_name))
                except:
                    pass
                
        with open(file_path, 'w') as f:
            json.dump(afk, f)
        
    @commands.command()
    async def afk(self, ctx, *, reason=None):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'db/afk.json')
        with open(file_path, 'r') as f:
            afk = json.load(f)

        if not reason:
            reason = 'None'
        
        await self.update_data(afk, ctx.message.author)
        afk[f'{ctx.author.id}']['AFK'] = 'True'
        afk[f'{ctx.author.id}']['reason'] = f'{reason}'
        afk[f'{ctx.author.id}']['time'] = int(time.time())
        afk[f'{ctx.author.id}']['mentions'] = 0

        await ctx.reply("You're now AFK. Send a message to remove it.")
        with open(file_path, 'w') as f:
            json.dump(afk, f)
        try:
            await ctx.author.edit(nick=f'[AFK] {ctx.author.display_name}')
        except:
            pass
