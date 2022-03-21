from redbot.core import commands
import re
import discord

URL_REGEX = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")



class Screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['ss'])
    async def screenshot(self, ctx, site):
        """Returns a screenshot of a site, this may not be accurate."""
        if not re.fullmatch(URL_REGEX, site):
            await ctx.send('Invalid URL')
            return
        e=discord.Embed(color=0xd3c1e3, timestamp=ctx.message.created_at)
        e.set_image(url=f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{site}")
        await ctx.send(embed=e)


