from .channels import Channels
from .owner import Owner


def setup(bot):
    bot.add_cog(Channels(bot))
   

def setup(bot):
    bot.add_cog(Owner(bot))
