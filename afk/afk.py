from redbot.core import commands
from .afks import afks
import discord
from discord.utils import get

def remove(afk):
    if '[AFK]' in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def afk(self, ctx, *, reason='No reason'):
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick=f'[AFK] {member.display_name}')
            except:
                pass

        afks[member.id] = reason
        await ctx.send(f'You are now AFK **{member.name}**. Send a message to remove it.')
 
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick=remove(message.author.display_name))
            except:
                pass
            await message.reply(f'Welcome back {message.author.name}. I have removed your AFK.')

        for id, reason in afks.items():
            member = get(message.guild.members, id=id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                e=discord.Embed(
                    title=f"{message.author.name} is AFK",
                    description=f"**Message:**\n{reason}"
                )
                await message.send(embed=e)


    
