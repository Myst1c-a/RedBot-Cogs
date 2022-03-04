from redbot.core import commands

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cch'], name='createchannel', help='Creates a channel.') 
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, channel_name, category : int = None):
        if category == None:
            category = None
        c = self.bot.get_channel(category)
        guild = ctx.message.guild
        await guild.create_text_channel(channel_name, category=c)
        await ctx.send(f'**{channel_name}** channel successfully created.')

    @commands.command(aliases=['cca'], name='createcategory', help='Creates a category.') 
    @commands.has_permissions(manage_channels=True)
    async def createcategory(self, ctx, *, category_name):
     await ctx.guild.create_category(category_name)
     await ctx.send(f'**{category_name}** category successfully created.')
