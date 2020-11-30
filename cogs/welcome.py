import discord
from discord.ext import commands
from utils.readabletime import getReadableTimeBetween
from main import main_color, CommunityRoleID, chatChannelId, ArtiFeZGuildIconUrl, modLogsChannelId
import datetime, random

def setup(bot):
    bot.add_cog(welcome(bot))

class welcome(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        await member.add_roles(discord.Object(CommunityRoleID))
        channel = self.bot.get_channel(chatChannelId)
        time = getReadableTimeBetween(member.created_at.timestamp(), datetime.datetime.utcnow().timestamp())
        time_split = time.split(",")
        e = discord.Embed(title="New Member!", color=main_color)
        e.description = f"• **Name**: {member.mention}\n" \
                        f"• **Account Created**: {time_split[0] + ' and ' + time_split[1]} ago.\n" \
                        f"• **Lucky Number**: {random.randint(1, 10)} <a:party_blob:757821206421438464>"
        e.set_author(name=str(member), icon_url=member.avatar_url)
        e.set_footer(text=self.bot.user.name, icon_url=ArtiFeZGuildIconUrl)
        await channel.send(embed=e)
        e = discord.Embed(title='**Welcome to *ArtiFeZ*!**', color=main_color)
        e.description = ""

    @commands.Cog.listener()
    async def on_member_remove(self, member : discord.Member):
        channel = self.bot.get_channel(modLogsChannelId)
        time = getReadableTimeBetween(member.joined_at.timestamp(), datetime.datetime.utcnow().timestamp())
        time_split = time.split(",")
        e = discord.Embed(title="Member Left", color=main_color)
        e.description = f"• **Name**: {member.mention}\n" \
                        f"• **Joined at**: {time_split[0] + ' and ' + time_split[1]} ago.\n" \
                        f"• **Roles ({len(member.roles[1:])})**: {', '.join(x.mention for x in member.roles[1:])}"
        e.set_author(name=str(member), icon_url=member.avatar_url)
        e.set_footer(text=self.bot.user.name, icon_url=ArtiFeZGuildIconUrl)
        return await channel.send(embed=e)