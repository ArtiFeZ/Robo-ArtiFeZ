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
ArtiFeZGuildIconUrl= "https://cdn.discordapp.com/icons/715126942294343700/a_f0571bc3d48dc0d401cf2a9dc9c01457.gif?size=1024"
bot                = commands.Bot(
command_prefix     = commands.when_mentioned_or("/", "."),
intents            = intents,
case_insensitive   = True
)
muteRoleID         = 765559649097089086
moderatorRoleId    = 767980191438995516
modLogsChannelId   = 716924699853979728
rulesChannelId     = 715165480666529812
bot.load_extension('jishaku')

async def pool_run():
    bot.pool = await asyncpg.create_pool(database='ArtiFeZ', password=database_pw, user='postgres')

loaded = 0
not_loaded = 0
for x in os.listdir('cogs'):
    if x.endswith(".py"):
        try:
            bot.load_extension("cogs." + x[:-3])
            loaded += 1
        except:
            not_loaded += 1
            pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over ArtiFeZ"))
    print(f"───────────────")
    print(f"Logged in as {str(bot.user)}")
    print(f"Successfully loaded {loaded}/{loaded + not_loaded} cogs")
    print(f"ArtiFeZ members: {len((bot.get_guild(ArtiFeZ_guild_id)).members)}")
    print(f"Average latency: {round(int(bot.latency * 1000))}ms")
    print(f"───────────────")

@bot.event
async def on_guild_join(guild):
    if guild.id != ArtiFeZ_guild_id:
        return await guild.leave()

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

bot.loop.run_until_complete(pool_run())
bot.run(str(token))