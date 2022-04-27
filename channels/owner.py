from redbot.core import commands
import typing


class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  
    @commands.command()
    @commands.is_owner()
    async def spy_server(
        self,
        ctx: commands.Context,
        guild: typing.Union[discord.Guild, int] = None,
        channel_member: str = None,
    ):
        """This is not really a spy command"""
        guild = guild or ctx.guild
        channel_member = channel_member or "members"
        URL = f"https://discord.com/api/guilds/{guild.id if isinstance(guild, discord.Guild) else guild}/widget.json"
        data = await self.bot.http_session.get(URL)
        json = await data.json()
        if "message" in json:
            return await ctx.reply(f"{ctx.author.mention} can not spy that server")
        name = json["name"]
        id_ = json["id"]
        instant_invite = json["instant_invite"]
        presence_count = json["presence_count"]

        embed_first = discord.Embed(
            title=name,
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow(),
        )
        if instant_invite:
            embed_first.url = instant_invite
        embed_first.set_footer(text=f"{id_}")
        embed_first.description = f"**Presence Count:** {presence_count}"
        em_list = [embed_first]

        for channel in json["channels"]:
            em_chan = discord.Embed(
                title=channel["name"],
                description=f"**Position:** {channel['position']}",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow(),
            ).set_footer(text=channel["id"])

            em_list.append(em_chan)

        em_list_member = [embed_first]

        for member in json["members"]:
            id_ = member["id"]
            username = member["username"]
            discriminator = member["discriminator"]
            avatar_url = member["avatar_url"]
            status = member["status"]
            vc = member["channel_id"] if "channel_id" in member else None
            suppress = member["suppress"] if "suppress" in member else None
            self_mute = member["self_mute"] if "self_mute" in member else None
            self_deaf = member["self_deaf"] if "self_deaf" in member else None
            deaf = member["deaf"] if "deaf" in member else None
            mute = member["mute"] if "mute" in member else None

            em = (
                discord.Embed(
                    title=f"Username: {username}#{discriminator}",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow(),
                )
                .set_footer(text=f"{id_}")
                .set_thumbnail(url=avatar_url)
            )
            em.description = f"**Status:** {status.upper()}\n**In VC?** {bool(vc)} ({'<#'+str(vc)+'>' if vc else None})"
            if vc:
                em.add_field(name="VC Channel ID", value=str(vc), inline=True)
                em.add_field(name="Suppress?", value=suppress, inline=True)
                em.add_field(name="Self Mute?", value=self_mute, inline=True)
                em.add_field(name="Self Deaf?", value=self_deaf, inline=True)
                em.add_field(name="Deaf?", value=deaf, inline=True)
                em.add_field(name="Mute?", value=mute, inline=True)
            em_list_member.append(em)
