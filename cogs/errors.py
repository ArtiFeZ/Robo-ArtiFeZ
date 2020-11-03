from discord.ext import commands
from discord import *

def setup(client):
    client.add_cog(errors(client))

class errors(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            raise error