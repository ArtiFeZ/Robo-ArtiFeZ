import discord
from discord.ext import commands
import json

config_read       = open("config.json", "r")
config            = json.load(config_read)
token             = config['token']
intents           = discord.Intents.all()
intents.presences = True
intents.members   = True
main_color        = 0x00000000
ArtiFeZ_guild_id  = 715126942294343700

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("?", "!", "-", "/", "."),
    intents=intents,
)
bot.load_extension('jishaku')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over ArtiFeZ"))
    print(f"Logged in as {bot.user.display_name + '#' + bot.user.discriminator}!")
    print(f"ArtiFeZ members: {len(bot.users)}")
    print(f"Average latency: {round(int(bot.latency * 1000))}ms")

@bot.command(name="ping", help="shows the latency of the bot, not yours.")
async def ping(ctx : commands.Context):
    e = discord.Embed(
        title="🏓  Ping!",
        description=f"Bot's Average Latency: **{round(int(bot.latency * 1000))}ms**"
    )
    e.set_footer(text="Robo-ArtiFeZ 🤖", icon_url=bot.user.icon_url)
    await ctx.send(embed=e)
    # await ctx.send("works!")
    return

bot.run(str(token))