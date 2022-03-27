from redbot.core import commands
import re
import discord

URL_REGEX = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")



class Screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(aliases=['ss'], invoke_without_command=True)
    async def screenshot(self):
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
    async def send(self, ctx, channel : discord.TextChannel, content):
        """Sends a discord attachment into a channel."""
        await channel.send(ctx.message.attachments[0].url)
        await ctx.send('Successfully sent the attachment.')
        
