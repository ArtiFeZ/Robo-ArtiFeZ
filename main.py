import discord
from discord.ext import commands
import json, os
import datetime
import asyncpg, re, asyncio, time
from typing import *
import utils.readabletime as rdTime
# print(discord.__version__)

config_read        = open("config.json", "r")
config             = json.load(config_read)
token              = config['token']
database_pw        = config['database_pw']
intents            = discord.Intents.default()
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
chatChannelId      = 715868519329300543
ApprovedRoleID     = 781079692174295060
CommunityRoleID    = 715212118181543998
ShowCaseChannelsID = [765053372947890176, 765054300178087938, 769955894456221696]
TeamRoleID         = 803291017822470186
AboutUs            = """・ArtifeZ is an Editing Team/Community, where you can showcase your work.
・We have a system where you can also purchase work from our [Verified Sellers](https://discordapp.com/channels/715126942294343700/782808652994052106).
・We are powered and presented by [SCYTES Esports](https://www.scytes.com).
・We also [host competitions](https://discordapp.com/channels/715126942294343700/743868715459936287) and help you grow better and bigger as an artist.
"""
bot.load_extension('jishaku')
TwitterEmoji       = "<:afzTwitter:783822204109586484>"
InstaEmoji         = "<:afzinsta:803483570240225280>"


async def pool_run():
    bot.pool = await asyncpg.create_pool(database='ArtiFeZ', password=database_pw, user='postgres')

loaded = 0
not_loaded = 0
for x in os.listdir('cogs'):
    if x.endswith(".py"):
        try:
            bot.load_extension("cogs." + x[:-3])
            loaded += 1
        except Exception as e:
            not_loaded += 1
            raise e


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over ArtiFeZ"))
    print(f"───────────────")
    print(f"Logged in as {str(bot.user)} ({bot.user.id})")
    print(f"Successfully loaded {loaded}/{loaded + not_loaded} cogs")
    print(f"ArtiFeZ members: {len((bot.get_guild(ArtiFeZ_guild_id)).members)}")
    print(f"Average latency: {round(int(bot.latency * 1000))}ms")
    print(f"───────────────")


@bot.event
async def on_guild_join(guild):
    if guild.id != ArtiFeZ_guild_id:
        ch = guild.text_channels[0]
        try:
            await ch.send('I am not supposed to be here!')
            return await guild.leave()
        except Exception as f:
            if isinstance(f, discord.Forbidden):
                pass
            return await guild.leave()
    else:
        pass


@bot.command(name="ping", help="shows the latency of the bot, not yours.")
async def ping(ctx : commands.Context):
    wsLatency = round(int(bot.latency * 1000))
    e2 = discord.Embed(
        title="🏓  Pong!",
        description=f"Websocket Latency: **{wsLatency}ms**\n",
        color=main_color
    )
    e2.set_footer(text=bot.user.name, icon_url=bot.user.avatar_url)
    aw = await ctx.send(embed=e2)
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