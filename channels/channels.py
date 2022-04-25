from redbot.core import commands

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['cch'])
    @commands.guild_only()
    @commands.permissions(manage_channels=True)
    async def createchannel(self, ctx):
        """Creates channels."""
        

    @createchannel.command()
    async def text(self, ctx, name, category : int = None):
        """Creates a text channel."""
        category = category or None
        c = self.bot.get_channel(category)
        guild = ctx.message.guild
        await guild.create_text_channel(name, category=c)
        await ctx.send(f'**{name}** channel successfully created.')


    @createchannel.command()
    async def voice(self, ctx, name, category : int = None):
        """Creates a voice channel."""
        category = category or None
        c = self.bot.get_channel(category)
        guild = ctx.message.guild
        await guild.create_voice_channel(name, category=c)
        await ctx.send(f'**{name}** channel successfully created.')


    @commands.command(aliases=['cca'], name='createcategory') 
    @commands.has_permissions(manage_channels=True)
    async def createcategory(self, ctx, *, category_name):
        """Creates a category channel."""
        await ctx.guild.create_category(category_name)
        await ctx.send(f'**{category_name}** category successfully created.')
