import discord
from discord.ext import commands
from main import *
import random

def setup(bot):
    bot.add_cog(rReactions(bot))

class rReactions(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        gld : discord.Guild = self.bot.get_guild(ArtiFeZ_guild_id)
        if message.author.bot: return
        emojis = gld.emojis
        remoji = random.choice(emojis)
        rnum = random.randint(1,8)
        rnum2 = random.randint(1,8)
        if rnum2 == rnum:
            await message.add_reaction(remoji)
        else:
            return
        await self.bot.process_commands(message)