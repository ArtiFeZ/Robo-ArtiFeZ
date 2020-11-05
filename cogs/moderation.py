import discord
from discord.ext import commands
import json, os
import datetime
import asyncpg, re, asyncio, time
import utils.readabletime as rdTime
from main import main_color, muteRoleID, moderatorRoleId, ArtiFeZ_guild_id, modLogsChannelId, ArtiFeZGuildIconUrl

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

def setup(bot):
    bot.add_cog(moderation(bot))

class moderation(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.unmute_on_time())

    @commands.Cog.listener()
    async def on_member_unmute(self, data: list):
        channel = self.bot.get_channel(modLogsChannelId)
        data = data[0]
        muted_at = int(data['muted_at'])
        unmute_at = int(data['unmute_at'])
        timestr = rdTime.getReadableTimeBetween(muted_at, unmute_at)
        embed = discord.Embed(
            title="Member Unmuted",
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
            title="Member Muted",
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
            return await ctx.send(f"{ctx.author.mention} Member not mentioned", embed=usageEmbed)
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

    @commands.command(name='unmute', help='Unmutes the member mentioned, if the member is muted.', aliases=['um'])
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
            title="Member Kicked"
        )
        e.add_field(
            name="Member kicked:",
            value=f"• **Name**: {member.name} - {member.mention}\n"
                  f"• **ID**: {member.id}\n"
                  f"• **Joined at**: {member.joined_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Created at**: {member.created_at.strftime('%d %b %Y at %I:%M %p')}\n"
                  f"• **Roles ({len(member.roles[:1])})**: {', '.join(x.mention for x in member.roles[:1])}",
            inline=False
        )
        e.add_field(
            name="Kicked by:",
            value=f"• **Name**: {kicked_by.name} - {kicked_by.mention}\n"
                  f"• **ID**: {kicked_by.id}\n"
                  f"• **Reason**: {reason}", inline=False
        )
        e.set_author(icon_url=ArtiFeZGuildIconUrl, name=self.bot.user.name)
        await channel.send(embed=e)

    @commands.command(name="kick", help="Kicks the member mentioned.")
    @commands.guild_only()
    @commands.has_role(moderatorRoleId)
    async def kick(self, ctx : commands.Context, member : discord.Member = None, reason : str = None):
        if member and reason:
            await member.kick(reason=reason)
            e2 = discord.Embed(color=main_color, title=f"Successfully kicked {str(member)}")
            await ctx.send(embed=e2)
            self.bot.dispatch("member_kick__", member=member, reason=reason, kicked_by=ctx.author)
        if not member:
            e = discord.Embed(title="You did not mention a member.", color=discord.Color.red())
            return await ctx.send(embed=e)
        elif not reason:
            e = discord.Embed(title="You did not mention a reason.", color=discord.Color.red())
            return await ctx.send(embed=e)
