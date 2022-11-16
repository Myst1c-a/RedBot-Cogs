from .afk import AFK


async def setup(bot):
    await bot.add_cog(AFK(bot))
