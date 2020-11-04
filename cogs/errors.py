from discord.ext import commands
from discord import *
from main import main_color

def setup(client):
    client.add_cog(errors(client))

class errors(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRole):
            return await ctx.send(embed=discord.Embed(color=main_color, title=f"This command requires the {', '.join(f'`{x}`' for x in error.missing_role)} role{'s' if len(error.missing_role) != 1 else ''}."))
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(embed=discord.Embed(color=main_color, title=f"This command cannot be used in private messages."))
        else:
            raise error