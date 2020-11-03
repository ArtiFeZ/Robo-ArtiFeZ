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



