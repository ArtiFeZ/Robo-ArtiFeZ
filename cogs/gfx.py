import discord
from discord.ext import commands
from main import main_color, ArtiFeZGuildIconUrl
from utils.tutorialEmbed import get_tutorial_embed
from utils.packsEmbed import get_packs_embed

def setup(bot):
    bot.add_cog(gfx(bot))

class gfx(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.group(name="gfx", case_insensitive=True)
    async def gfx(self, ctx: commands.Context) :
        if ctx.invoked_subcommand is None :
            cog: commands.Cog = self.bot.get_cog('gfx')
            e = discord.Embed(color=main_color, title="GFX Category")
            for command in cog.walk_commands() :
                if not isinstance(command, commands.Group) :
                    e.add_field(
                        name=f".{command.full_parent_name} {command.name} {command.signature}",
                        value="⮑  " + command.help,
                        inline=False
                    )
            e.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            return await ctx.send(embed=e)
        else :
            pass

    @gfx.command(name="tutorials", aliases=['tuts', 'tut'],
                 help="Gives a neat list of some major gfx tutorials, according to the level of difficulty.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _gfx_tuts(self, ctx: commands.Context) :
        """Gives a neat list of some major gfx tutorials, according to the level of difficulty."""
        beginners = {
            "None yet" : "None yet"
        }
        moderate = {
            "None yet" : "None yet"
        }
        experienced = {
            "None yet" : "None yet"
        }
        embed = get_tutorial_embed(beginners, moderate, experienced, "GFX Tutorials")
        return await ctx.send(embed=embed)

    @gfx.command(name="packs", help="Gives a list of some popular gfx packs.", aliases=['pack', 'p'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def _gfx_packs(self, ctx: commands.Context) :
        packs: dict = {
            "None yet" : "None yet"
        }
        e = get_packs_embed(packs, "GFX Packs")
        return await ctx.send(embed=e)