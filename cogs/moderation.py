import discord
from discord.ext import commands
import json, os
import datetime
import asyncpg, re, asyncio, time
import utils.readabletime as rdTime
from main import main_color, rulesChannelId, muteRoleID, moderatorRoleId, ArtiFeZ_guild_id, modLogsChannelId, ArtiFeZGuildIconUrl
from typing import *

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def setup(bot):
    bot.add_cog(moderation(bot))


class moderation(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.unmute_on_time())
        self.bot.loop.create_task(self.delete_warns())

    @commands.Cog.listener()
    async def on_member_unmute(self, data: list):
        channel = self.bot.get_channel(modLogsChannelId)
        data = data[0]
        muted_at = int(data['muted_at'])
        unmute_at = int(data['unmute_at'])
        timestr = rdTime.getReadableTimeBetween(muted_at, unmute_at)
        embed = discord.Embed(
            #title="Member Unmuted",
            color=main_color,
        )
        embed.add_field(
            name="Member unmuted:",
            value=f"<@{data['user_id']}> ({data['user_id']})",
            inline=False
        )
        embed.add_field(
            name="Was muted by:",
            value=f"<@{data['muted_by']}> ({data['muted_by']})",
            inline=False
        )
        embed.add_field(
            name="Was muted for:",
            value=f"{timestr}",
            inline=False
        )
        embed.add_field(
            name="Reason:",
            value=f"{data['reason']}",
            inline=False
        )
        embed.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        # embed.timestamp = datetime.datetime.fromtimestamp(data['muted_at'])
        member = self.bot.get_user(int(data['muted_by']))
        embed.set_footer(text=f"Muted by {str(member)}", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_mute(self, data : list):
        channel = self.bot.get_channel(modLogsChannelId)
        data = data[0]
        muted_at = int(data['muted_at'])
        unmute_at = int(data['unmute_at'])
        timestr = rdTime.getReadableTimeBetween(muted_at, unmute_at)
        embed = discord.Embed(
            #title="Member Muted",
            color=main_color,
        )
        embed.add_field(
            name="Member muted:",
            value=f"<@{data['user_id']}> ({data['user_id']})",
            inline=False
        )
        embed.add_field(
            name="Muted by:",
            value=f"<@{data['muted_by']}> ({data['muted_by']})",
            inline=False
        )
        embed.add_field(
            name="Duration:",
            value=f"{timestr}",
            inline=False
        )
        embed.add_field(
            name="Reason:",
            value=f"{data['reason']}",
            inline=False
        )
        embed.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        # embed.timestamp = datetime.datetime.fromtimestamp(data['muted_at'])
        member = self.bot.get_user(id = int(data['muted_by']))
        embed.set_footer(text=f"Muted by {str(member)}", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def delete_warns(self):
        while True:
            await self.bot.wait_until_ready()
            await self.bot.pool.execute("DELETE FROM warns WHERE warns <= 0")
            await asyncio.sleep(60)

    async def unmute_on_time(self):
        while True:
            await asyncio.sleep(20 * 10)
            # print("unmute_on_time event called ")
            await self.bot.wait_until_ready()
            all = await self.bot.pool.fetch("SELECT * FROM mute")
            all_unmuted = [x['unmute_at'] for x in all]
            for i in all_unmuted:
                if int(datetime.datetime.now().timestamp()) > i:
                    fetch  = await self.bot.pool.fetch("SELECT * FROM mute WHERE unmute_at = $1", i)
                    if not fetch[0]['unmuted']:
                        guild : discord.Guild = self.bot.get_guild(ArtiFeZ_guild_id)
                        member = guild.get_member(int(fetch[0]['user_id']))
                        roles_ids : list = fetch[0]['roles_before']
                        for i in roles_ids:
                            try:
                                await member.add_roles(discord.Object(id=i), atomic=True)
                            except:
                                pass
                        await member.remove_roles(discord.Object(id=muteRoleID), atomic=True)
                        query2 = "UPDATE mute SET unmuted = $1 WHERE user_id = $2"
                        await self.bot.pool.execute(query2, True, str(member.id))
                        self.bot.dispatch("member_unmute", data=fetch)
                        continue
                    if fetch[0]['unmuted']: continue

    class TimeConverter(commands.Converter):
        async def convert(self, ctx, argument):
            self.argument = argument
            args = self.argument.lower()
            matches = re.findall(time_regex, args)
            time = 0
            for v, k in matches:
                try:
                    time += time_dict[k] * float(v)
                except KeyError:
                    raise commands.BadArgument("{} is an invalid time.py-key! h/m/s/d are valid!".format(k))
                except ValueError:
                    raise commands.BadArgument("{} is not a number!".format(v))
            return time

    @commands.command(name='mute')
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.has_role(moderatorRoleId)
    async def mute(self, ctx, duration: TimeConverter = None, member: discord.Member = None, *,
                   reason: str = "Reason not provided."):
        '''Mutes the member mentioned for the time mentioned.'''
        ugh = '"'
        usageEmbed = discord.Embed(color=discord.Color.red(),
                                   title="Incorrect  usage!",
                                   description="Usage:\n"
                                               "• `.mute [duration] [member] [reason]`\n• `.mute 1d2h5m 12344566721 he did not follow #2 rule`\n\n"
                                               "Note:\n"
                                               "• Duration can contain: `m`, `h`, `d` and `s`\n"
                                               f"• Member can contain: `@member`, `{ugh}member name{ugh}`, `member ID (12311414)`\n"
                                               "• Minimum mute time: `10m`\n"
                                               "• You need to Provide a valid reason.")
        if not duration:
            return await ctx.send(f"{ctx.author.mention} Duration Not Provided.", embed=usageEmbed)
        elif not member:
            return await ctx.send(f"{ctx.author.mention} Member Not Provided.", embed=usageEmbed)
        # elif int(duration) < 600:
        #     return await ctx.send(f"{ctx.author.mention} Duration less than 10 minutes.", embed=usageEmbed)
        elif reason == "Reason not provided.":
            return await ctx.send(f"{ctx.author.mention} Reason Not Provided.", embed=usageEmbed)
        elif duration and member:
            muted_at = int(ctx.message.created_at.timestamp())
            unmute_at = int((ctx.message.created_at + datetime.timedelta(seconds=int(duration))).timestamp())
            timestr = rdTime.getReadableTimeBetween(muted_at, unmute_at)
            sendEmbed = discord.Embed(color=main_color, title=f"Muting {str(member)}...")
            send: discord.Message = await ctx.send(embed=sendEmbed)
            roles_before: list = [x.id for x in member.roles]
            if muteRoleID in roles_before:
                e1 = discord.Embed(color=main_color,
                                   title="Already Muted!",
                                   description=f"**{str(member)}** has already been muted!")
                return await ctx.send(embed=e1)
            query = "INSERT INTO mute (user_id, muted_at, unmute_at, roles_before, unmuted, muted_by, reason) VALUES  ($1, $2, $3, $4, $5, $6, $7)"
            await self.bot.pool.execute(query, str(member.id), muted_at, unmute_at, roles_before, False, str(ctx.author.id), reason)
            for x in member.roles[1:]:
                try:
                    await member.remove_roles(x)
                except:
                    pass
            await member.add_roles(discord.Object(id=muteRoleID), atomic=True)
            embed = discord.Embed(color=main_color, title=f"Success", description=f"Successfully muted {str(member.mention)}\n"
                                                                                  f"• For:  **{timestr}**.\n"
                                                                                  f"• Reason: **{reason}**")
            embed.set_footer(text=f"{str(member.name)} will be unmuted:")
            embed.timestamp = ctx.message.created_at + datetime.timedelta(seconds=int(duration))
            fetch = await self.bot.pool.fetch("SELECT * FROM mute WHERE unmute_at = $1 AND muted_by = $2", unmute_at, str(ctx.author.id))
            self.bot.dispatch("member_mute", data=fetch)
            return await send.edit(content="", embed=embed, delete_after=int(duration))

    @commands.command(name='unmute', help='Unmutes the member provided, if the member is muted.', aliases=['um'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.has_role(moderatorRoleId)
    async def unmute(self, ctx: commands.Context, *, member: discord.Member = None):
        if not member:
            e0 = discord.Embed(title=f"{ctx.author.name} You did not provide a member to unmute!", color=main_color)
            return await ctx.send(embed=e0)
        if member:
            all_roles_ids = [i.id for i in ctx.guild.roles]
            member_roles_ids = [i.id for i in member.roles]
            if muteRoleID in all_roles_ids and muteRoleID in member_roles_ids:
                sendEmbed = discord.Embed(color=main_color, title=f"Unmuting {str(member)}...")
                send: discord.Message = await ctx.send(embed=sendEmbed)
                query = "SELECT * FROM mute WHERE user_id = $1 AND unmuted = $2"
                dbEntry = await self.bot.pool.fetch(query, str(member.id), False)
                await member.remove_roles(discord.Object(id=muteRoleID), atomic=False)
                prevRoles = dbEntry[0]['roles_before']
                for i in prevRoles:
                    try:
                        if i not in member_roles_ids:
                            await member.add_roles(discord.Object(id=i), atomic=True)
                        else:
                            pass
                    except:
                        pass
                query2 = "UPDATE mute SET unmuted = $1 WHERE user_id = $2"
                await self.bot.pool.execute(query2, True, str(member.id))
                self.bot.dispatch("member_unmute", data=dbEntry)
                return await send.edit(
                    embed=discord.Embed(title=f"Successfully unmuted {str(member)}", color=main_color))
            elif muteRoleID not in member_roles_ids:
                return await ctx.send(embed=discord.Embed(title=f"{str(member)} is not muted!", color=main_color))
            else:
                return await ctx.send(
                    embed=discord.Embed(title=f"There was an error! Please contact Videro#9999", color=main_color))

    @commands.Cog.listener()
    async def on_member_kick__(self, member : discord.Member, reason : str, kicked_by : discord.Member):
        channel = self.bot.get_channel(modLogsChannelId)
        e = discord.Embed(
            color=main_color,
            # title="Member Kicked"
        )
        e.add_field(
            name="Member kicked:",
            value=f"• **Name**: {member.name} - {member.mention}\n"
                  f"• **ID**: {member.id}\n"
                  f"• **Joined at**: {member.joined_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Created at**: {member.created_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Roles ({len(member.roles[1:])})**: {', '.join(x.mention for x in member.roles[1:])}",
            inline=False
        )
        e.add_field(
            name="Kicked by:",
            value=f"• **Name**: {kicked_by.name} - {kicked_by.mention}\n"
                  f"• **ID**: {kicked_by.id}\n"
                  f"• **Reason**: {reason}", inline=False
        )
        e.set_footer(text="Kicked at:")
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_ban__(self, member: discord.Member, reason: str, banned_by: discord.Member):
        channel = self.bot.get_channel(modLogsChannelId)
        e = discord.Embed(
            color=main_color,
            # title="Member Kicked"
        )
        e.add_field(
            name="Member banned:",
            value=f"• **Name**: {member.name} - {member.mention}\n"
                  f"• **ID**: {member.id}\n"
                  f"• **Joined at**: {member.joined_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Created at**: {member.created_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Roles ({len(member.roles[1:])})**: {', '.join(x.mention for x in member.roles[1:])}",
            inline=False
        )
        e.add_field(
            name="Banned by:",
            value=f"• **Name**: {banned_by.name} - {banned_by.mention}\n"
                  f"• **ID**: {banned_by.id}\n"
                  f"• **Reason**: {reason}", inline=False
        )
        e.set_footer(text="Banned at:")
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_unban__(self, member: discord.Member, reason: str, unbanned_by: discord.Member):
        channel = self.bot.get_channel(modLogsChannelId)
        e = discord.Embed(
            color=main_color,
        )
        e.add_field(
            name="Member unbanned:",
            value=f"• **Name**: {member.name} - {member.mention}\n"
                  f"• **ID**: {member.id}\n"
                  f"• **Created at**: {member.created_at.strftime('%d %b %Y at %I:%M %p')}",
            inline=False
        )
        e.add_field(
            name="Unbanned by:",
            value=f"• **Name**: {unbanned_by.name} - {unbanned_by.mention}\n"
                  f"• **ID**: {unbanned_by.id}\n"
                  f"• **Reason**: {reason}", inline=False
        )
        e.set_footer(text="Unbanned at:")
        e.timestamp = datetime.datetime.utcnow()
        e.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        await channel.send(embed=e)

    @commands.command(name="kick", help="Kicks the member provided.", aliases = ['k'])
    @commands.guild_only()
    @commands.has_role(moderatorRoleId)
    async def _kick(self, ctx : commands.Context, member : discord.Member = None, *, reason : str = None):
        if member and reason:
            await member.kick(reason=reason)
            e2 = discord.Embed(color=main_color, title=f"Successfully kicked {str(member)}")
            await ctx.send(embed=e2)
            self.bot.dispatch("member_kick__", member=member, reason=reason, kicked_by=ctx.author)
        if not member:
            e = discord.Embed(title="You did not provide a member.", color=discord.Color.red())
            return await ctx.send(embed=e)
        elif not reason:
            e = discord.Embed(title="You did not provide a reason.", color=discord.Color.red())
            return await ctx.send(embed=e)

    @commands.command(name="ban", help="Bans the member provided.", aliases = ['b'])
    @commands.guild_only()
    @commands.has_role(moderatorRoleId)
    async def ban_(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if member and reason:
            await member.ban(reason=reason)
            e2 = discord.Embed(color=main_color, title=f"Successfully banned {str(member)}")
            await ctx.send(embed=e2)
            self.bot.dispatch("member_ban__", member=member, reason=reason, banned_by=ctx.author)
        if not member:
            e = discord.Embed(title="You did not provide a member.", color=discord.Color.red())
            return await ctx.send(embed=e)
        elif not reason:
            e = discord.Embed(title="You did not provide a reason.", color=discord.Color.red())
            return await ctx.send(embed=e)

    @commands.command(name="unban", help="Unbans the member provided.", aliases=['ub'])
    @commands.guild_only()
    @commands.has_role(moderatorRoleId)
    async def unban_(self, ctx: commands.Context, member: int = None, *, reason: str = None):
        if member and reason:
            bans : tuple = await ctx.guild.bans()
            member = await self.bot.fetch_user(member)
            users = []
            for i in bans:
                users.append(i[1])
            if member in users:
                await ctx.guild.unban(member, reason=reason)
                e2 = discord.Embed(color=main_color, title=f"Successfully unbanned {str(member)}")
                await ctx.send(embed=e2)
                return self.bot.dispatch("member_unban__", member=member, reason=reason, unbanned_by=ctx.author)
            if member not in users:
                e3 = discord.Embed(title=f"{str(member)} is not banned.", color=discord.Color.red())
                return await ctx.send(embed=e3)
        if not member:
            e = discord.Embed(title="You did not give a user's ID.", color=discord.Color.red())
            return await ctx.send(embed=e)
        elif not reason:
            e = discord.Embed(title="You did not provide a reason.", color=discord.Color.red())
            return await ctx.send(embed=e)

    @commands.command(name="warn", help="Warns the member provided.", aliases=["w"])
    @commands.guild_only()
    @commands.has_role(moderatorRoleId)
    async def _warn(self, ctx : commands.Context, member : discord.Member = None , *, reason : str = None):
        if member and reason:
            query = "SELECT * FROM warns WHERE user_id = $1"
            check = await self.bot.pool.fetch(query, member.id)
            if check:
                query2 = "UPDATE warns SET warns = $1 + 1 WHERE user_id = $2"
                await self.bot.pool.execute(query2, check[0]['warns'], member.id)
                if str(check[0]['warns'] + 1).endswith("1"):
                    x = "st"
                elif str(check[0]['warns'] + 1).endswith("2"):
                    x = "nd"
                elif str(check[0]['warns'] + 1).endswith("3"):
                    x = "rd"
                elif str(check[0]['warns'] + 1).endswith("11"):
                    x = "th"
                else:
                    x = "th"
                e3 = discord.Embed(color=main_color, title=f"",
                                   description=f"**Successfully warned {str(member)}. This is their {check[0]['warns'] + 1}{x} warning.**")
                await member.send(embed=discord.Embed(color=main_color,
                                                      title="You have been warned.",
                                                      description=f"You have been warned in **{ctx.guild.name}**.\n"
                                                                  f"Reason: **{reason}**\n"
                                                                  f"Warned by: **{str(ctx.author)}**\n"
                                                                  f"This is your **{check[0]['warns'] + 1}{x}** warning.\n"
                                                                  f"Make sure to check <#{rulesChannelId}> for info on the warn system.",
                                                      timestamp=datetime.datetime.utcnow())
                                  .set_footer(text="Warned at")
                                  .set_author(name=self.bot.user.name, icon_url=ctx.guild.icon_url))
                return await ctx.send(embed=e3)
            if not check:
                query3 = "INSERT INTO warns (warns, user_id) VALUES (1, $1)"
                await self.bot.pool.execute(query3, member.id)
                e3 = discord.Embed(color=main_color, description=f"**Successfully warned {str(member)}. This is their 1st warning.**")
                await member.send(embed=discord.Embed(color=main_color,
                                                      title="You have been warned.",
                                                      description=f"You have been warned in **{ctx.guild.name}**.\n"
                                                                  f"Reason: **{reason}**\n"
                                                                  f"Warned by: **{str(ctx.author)}**\n"
                                                                  f"This is your first warning.\n"
                                                                  f"Make sure to check <#{rulesChannelId}> for info on the warn system.",
                                                      timestamp=datetime.datetime.utcnow())
                                  .set_footer(text="Warned at")
                                  .set_author(name=self.bot.user.name, icon_url=ctx.guild.icon_url))
                return await ctx.send(embed=e3)
        elif not member:
            e3 = discord.Embed(color = discord.Color.red(), title="You did not provide a member.")
            return await ctx.send(embed=e3)
        elif not reason:
            e3 = discord.Embed(color = discord.Color.red(), title="You did not provide a reason.")
            return await ctx.send(embed=e3)

    @commands.command(name="warns", help="Shows the warsn of the member mentioned.", aliases=["warnings", "showwarns", "sw"])
    @commands.has_role(moderatorRoleId)
    @commands.guild_only()
    async def _warns(self, ctx : commands.Context, member : discord.Member = None):
        user_id = member.id
        query = "SELECT * FROM warns WHERE user_id = $1"
        fetch = await self.bot.pool.fetch(query, user_id)
        if fetch:
            e = discord.Embed(color=main_color, title=f"{str(member)} has {fetch[0]['warns']} warning{'' if int(fetch[0]['warns']) == 1 else 's'}")
            return await ctx.send(embed=e)
        if not fetch:
            e = discord.Embed(color=main_color, title=f"{str(member)} has no warnings")
            return await ctx.send(embed=e)

    @commands.command(name="clearwarns", help="Clears the amount of warns specified from the member specified", aliases=['cw'])
    @commands.has_role(moderatorRoleId)
    @commands.guild_only()
    async def _clearwarns(self, ctx: commands.Context, member : discord.Member = None, warns : int = None):
        helpEmbed = discord.Embed(color=main_color, description='```py\n.cw [member] [number of warns]\n.cw PHYMO_ROCKS 3\n.cw 1212316161231 5\n```')
        if member and warns:
            user_id = member.id
            query = "SELECT * FROM warns WHERE user_id = $1"
            fetch = await self.bot.pool.fetch(query, user_id)
            if fetch:
                query2 = "UPDATE warns SET warns = $1 WHERE user_id = $2"
                await self.bot.pool.execute(query2, int(fetch[0]['warns']) - warns, user_id)
                e3 = discord.Embed(color=main_color, description=f"**Successfully cleared {warns} warnings from {str(member)}.**\n"
                                                                 f"**{str(member)} now has {(fetch[0]['warns'] - warns) if (fetch[0]['warns'] - warns) >= 0 else 0} warnings.**")
                return await ctx.send(embed=e3)
            if not fetch:
                e2 = discord.Embed(color=main_color, title=f"{str(member)} has no warnings.")
                return await ctx.send(embed=e2)
        if not member:
            return await ctx.send(content=f"{ctx.author.mention}, you did not specify a member.", embed=helpEmbed)
        if not warns:
            return await ctx.send(content=f"{ctx.author.mention}, you did not specify number of warns.", embed=helpEmbed)

    @commands.command(name="resetwarns", help="Clears the amount of warns specified from the member specified", aliases=['rw'])
    @commands.has_role(moderatorRoleId)
    @commands.guild_only()
    async def _resetwarns(self, ctx: commands.Context, member: discord.Member = None):
        helpEmbed = discord.Embed(color=main_color,
                                  description='```py\n.rw [member]\n.rw PHYMO_ROCKS\n.rw 1212316161231\n```')
        if member:
            user_id = member.id
            query = "SELECT * FROM warns WHERE user_id = $1"
            fetch = await self.bot.pool.fetch(query, user_id)
            if fetch:
                query2 = "DELETE FROM warns WHERE user_id = $1"
                await self.bot.pool.execute(query2, user_id)
                e3 = discord.Embed(color=main_color,
                                   description=f"**Successfully removed all warnings from {str(member)}.**")
                return await ctx.send(embed=e3)
            if not fetch:
                e2 = discord.Embed(color=main_color, title=f"{str(member)} has no warnings.")
                return await ctx.send(embed=e2)
        if not member:
            return await ctx.send(content=f"{ctx.author.mention}, you did not specify a member.", embed=helpEmbed)
