import discord
from discord.ext import commands
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

class AFKCog(commands.Cog):
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
                mentionz = afk[f'{message.author.id}']['mentions']

                embed = discord.Embed(title=f"Welcome Back!", description=f"While you were AFK you recieved **{mentionz}** pings.", color=0xd3c1e3)
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
        
    @commands.command(aliases=['eyefkay'])
    async def afk(self, ctx, *, reason=None):
        """AFK command"""
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'db/afk.json')
        with open(file_path, 'r') as f:
            afk = json.load(f)

        if not reason:
            reason = 'None'
        
        await self.update_data(afk, ctx.message.author)
        afk[f'{ctx.author.id}']['user'] = f"{ctx.message.author}"
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
        
    @commands.command(aliases=['afkl'])
    @commands.is_owner()
    async def afklist(self, ctx):
        """A list of AFK users, restricted to the bot owner only"""
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'db/afk.json')
        with open(file_path, 'r') as f:
            afk = json.load(f)
        afkl = json.dumps(afk, indent=4)
        await ctx.send(f"```json\n{afkl}\n```")
