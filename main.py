import discord
from discord.ext import commands
import json, os
import datetime
import asyncpg, re, asyncio, time
import utils.readabletime as rdTime

config_read        = open("config.json", "r")
config             = json.load(config_read)
token              = config['token']
database_pw        = config['database_pw']
intents            = discord.Intents.all()
intents.presences  = True
intents.members    = True
main_color         = 0x18adff
ArtiFeZ_guild_id   = 715126942294343700
bot                = commands.Bot(
command_prefix     = commands.when_mentioned_or("?", "!", "-", "/", "."),
intents            = intents,
)
muteRoleID         = 765559649097089086
moderatorRoleId    = 767980191438995516
bot.load_extension('jishaku')

async def pool_run():
    bot.pool = await asyncpg.create_pool(database='ArtiFeZ', password=database_pw, user='postgres')

for x in os.listdir('cogs'):
    if x.endswith(".py"):
        bot.load_extension("cogs." + x[:-3])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over ArtiFeZ"))
    print(f"Logged in as {str(bot.user)}!")
    print(f"ArtiFeZ members: {len(bot.users)}")
    print(f"Average latency: {round(int(bot.latency * 1000))}ms")

@bot.command(name="ping", help="shows the latency of the bot, not yours.")
async def ping(ctx : commands.Context):
    wsLatency = round(int(bot.latency * 1000))
    e = discord.Embed(
        title="🏓  Pong!",
        description=f"Websocket Latency: **{wsLatency}ms**\n",
        color=main_color
    )
    e.set_footer(text=bot.user.name, icon_url=bot.user.avatar_url)
    aw = await ctx.send(embed=e)
    x = datetime.datetime.utcnow() - aw.created_at
    responseTime = round(x.microseconds / 1000)
    e2 = discord.Embed(
        title="🏓  Pong!",
        description=f"Websocket Latency: **{wsLatency}ms**\n"
                    f"Response Time: **{responseTime}ms**",
        color=main_color
    )
    e2.set_footer(text=bot.user.name, icon_url=bot.user.avatar_url)
    return await aw.edit(embed=e2)
    # await ctx.send("works!")

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        self.argument = argument
        args = self.argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time.py-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

@bot.command(name='mute')
@commands.cooldown(1, 3, commands.BucketType.member)
@commands.has_role(moderatorRoleId)
async def mute(ctx, duration : TimeConverter = None, member: discord.Member = None, *, reason : str = "Reason not provided."):
    '''Mutes the member mentioned for the time mentioned.'''
    ugh = '"'
    usageEmbed = discord.Embed(color=discord.Color.red(),
                               title="Incorrect usage!",
                               description="Usage:\n"
                                           "`.mute [duration] [member] [reason]` - `.mute 1d2h5m 12344566721 he did not follow #x rule`\n\n"
                                           "Note:"
                                           "• Duration can contain: `m`, `h`, `d` and `s`\n"
                                          f"• Member can contain: `@member`, `{ugh}member name{ugh}`, `member ID (12311414)`\n"
                                           "• Minimum mute time: `10m`\n"
                                           "• You need to Provide a valid reason.")
    if not duration:
        return await ctx.send(embed=usageEmbed)
    elif not member:
        return await ctx.send(embed=usageEmbed)
    elif int(duration) < 600:
        return await ctx.send(embed=usageEmbed)
    elif reason == "Reason not provided.":
        return await ctx.send(embed=usageEmbed)
    elif duration and member:
        muted_at = int(time.time())
        unmute_at = int((ctx.message.created_at + datetime.timedelta(seconds = int(duration))).timestamp())
        timestr = rdTime.getReadableTimeBetween(unmute_at, muted_at)
        sendEmbed = discord.Embed(color=main_color, title=f"Muting {str(member)} for {timestr}.")
        send : discord.Message = await ctx.send(embed=sendEmbed)
        roles_before : list = [x.id for x in member.roles]
        if muteRoleID in roles_before:
            e1 = discord.Embed(color=main_color,
                               title="Already Muted!",
                               description=f"**{str(member)}** has already been muted!")
            return await ctx.send(f"**{str(member)}** is already muted.")
        query = "INSERT INTO mute (user_id, muted_at, unmute_at, roles_before, unmuted, muted_by) VALUES ($1, $2, $3, $4, $5, $6)"
        await bot.pool.execute(query, str(member.id), muted_at, unmute_at, roles_before, False, str(ctx.author.id))
        try:
            for x in member.roles:
                if x.id != muteRoleID:
                    await member.remove_roles(x)
        except: # server booster role
            pass
        await member.add_roles(discord.Object(id=muteRoleID), atomic=True)
        embed = discord.Embed(color=main_color, title=f"Successfully muted {str(member)} for {timestr}.")
        embed.set_footer(text=f"{str(member)} will be unmuted at")
        embed.timestamp = ctx.message.created_at + datetime.timedelta(seconds = int(duration))
        return await send.edit(content="", embed=embed, delete_after = int(duration))

@bot.command(name='unmute', help='Unmutes the member mentioned, if the member is muted.', aliases=['um'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.member)
@commands.has_role(moderatorRoleId)
async def unmute(ctx : commands.Context, member: discord.Member = None):
    if not member:
        e0 = discord.Embed(title=f"{ctx.author.name} You did not provide a member to unmute!", color=main_color)
        return await ctx.send(embed=e0)
    if member:
        all_roles_ids = [i.id for i in ctx.guild.roles]
        member_roles_ids = [i.id for i in member.roles]
        if muteRoleID in all_roles_ids and muteRoleID in member_roles_ids:
            query = "SELECT FROM mute WHERE user_id = $1 AND unmuitted = $2"
            dbEntry = await bot.pool.fetch(query, str(member.id), False)
            await member.remove_roles(discord.Object(id=muteRoleID), atomic=False)
            prevRoles = dbEntry[0]['roles_before']
            for i in prevRoles:
                try:
                    await member.add_roles(discord.Object(id=i), atomic=True)
                except:
                    pass
            query2 = "UPDATE mute SET unmuted = $1 WHERE user_id = $2"
            await bot.pool.execute(query2, True, str(member.id))
            return await ctx.send(embed=discord.Embed(title=f"Successfully unmuted {str(member)}", color=main_color))
        elif muteRoleID not in member_roles_ids:
            return await ctx.send(embed=discord.Embed(title=f"{str(member)} is not muted!", color=main_color))
        else:
            return await ctx.send(embed=discord.Embed(title=f"There was an error! Please contact Videro#9999", color=main_color))

bot.loop.run_until_complete(pool_run())
bot.run(str(token))