import discord
from discord.ext import commands
import json

config_read = open("config.json", "r")
config = json.load(config_read)
token = config['token']

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(tuple(("?", "!", "-", "/", "."))),
    intents=intents,
)

ArtiFeZ_guild_id = 715126942294343700

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.display_name + '#' + bot.user.discriminator}!")
    print(f"ArtiFeZ members: {len(bot.guilds)}")
    print(f"Average latency: {round(int(bot.latency * 1000))}ms")

@bot.event
async def on_message(message : discord.Message):
    if message.guild.id != ArtiFeZ_guild_id:
        return
    else:
        pass


bot.run(str(token))