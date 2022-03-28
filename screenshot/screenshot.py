from redbot.core import commands
import re
import discord
import asyncio

URL_REGEX = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")



class Screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(aliases=['ss'], invoke_without_command=True)
    async def screenshot(self, ctx):
        """Screenshot related commands."""
        
    @screenshot.command()
    async def link(self, ctx, site):
        """Converts a URL into a embedded image."""
        if not re.fullmatch(URL_REGEX, site):
            await ctx.send('Invalid URL')
            return
        e=discord.Embed(color=0xd3c1e3, timestamp=ctx.message.created_at)
        e.set_image(url=f"https://api.popcat.xyz/screenshot?url={site}")
        await ctx.send(embed=e)
        
    @screenshot.command()
    async def send(self, ctx, channel : discord.TextChannel, content = None):
        """Sends a discord attachment into a channel."""
        if content == None:
            e=discord.Embed(color=0xd3c1e3)
            e.set_image(url=ctx.message.attachments[0].url)
            await channel.send(embed=e)
            await ctx.message.add_reaction('✅')
            await asyncio.sleep(0.5)
            await ctx.message.delete()
            return
        else:
            e=discord.Embed(description=content, color=0xd3c1e3)
            e.set_image(url=ctx.message.attachments[0].url)
            await channel.send(embed=e)
            await ctx.message.add_reaction('✅')
            await asyncio.sleep(0.5)
            await ctx.message.delete()
