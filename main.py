import discord
from discord.ext import commands
import json, os
from datetime import datetime

config_read       = open("config.json", "r")
config            = json.load(config_read)
token             = config['token']
intents           = discord.Intents.all()
intents.presences = True
intents.members   = True
main_color        = 0x18adff
ArtiFeZ_guild_id  = 715126942294343700

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("?", "!", "-", "/", "."),
    intents=intents,
)
bot.load_extension('jishaku')

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
    x = datetime.utcnow() - ctx.message.created_at
    responseTime = round(x.microseconds / 1000)
    wsLatency = round(int(bot.latency * 1000))
    e = discord.Embed(
        title="🏓  Pong!",
        description=f"Websocket Latency: **{wsLatency}ms**\n"
                    f"Response Time: **{responseTime}ms**",
        color=main_color
    )
    e.set_footer(text=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=e)
    # await ctx.send("works!")
    return

bot.run(str(token))