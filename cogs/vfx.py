import discord
from discord.ext import commands
from main import main_color, ArtiFeZGuildIconUrl
from utils.tutorialEmbed import get_tutorial_embed

def setup(bot):
    bot.add_cog(vfx(bot))

class vfx(commands.Cog):
    """"Command related to VFX like Tutorials, Packs, etc."""

    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.group(name="vfx", case_insensitive=True)
    async def vfx(self, ctx : commands.Context):
        if ctx.invoked_subcommand is None:
            cog : commands.Cog = self.bot.get_cog('vfx')
            e = discord.Embed(color=main_color, title="FX Category")
            for command in cog.walk_commands():
                if not isinstance(command, commands.Group):
                    e.add_field(
                        name=f"{ctx.prefix}{command.full_parent_name} {command.name} {command.signature}",
                        value="⮑  " + command.help,
                        inline=False
                    )
            e.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            return await ctx.send(embed=e)
        else:
            pass

    @vfx.command(name="tutorials", aliases=['tuts', 'tut'], help="Gives a neat list of some major vfx tutorials, according to the level of difficulty.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _vfx_tuts(self, ctx : commands.Context):
        """Gives a neat list of some major vfx tutorials, according to the level of difficulty."""
        beginners = {
            "Basic Introduction"      : "https://www.youtube.com/watch?v=ShHtpCUjU1w",
            "How to have Flow"        : "https://www.youtube.com/watch?v=2ihziwEOfzQ",
            "How to do Pan and Crop"  : "https://www.youtube.com/watch?v=sqyFfIeSIH0",
            "How to do Impact"        : "https://www.youtube.com/watch?v=1nlEYIIu9Xs",
            "How to do Basic Effects" : "https://www.youtube.com/watch?v=yMZgZauYb24"
        }
        moderate = {
            "How to do 3D Text"                 : "https://www.youtube.com/watch?v=alQthirJ51g",
            "How to do Effective Pan and Crop"  : "https://www.youtube.com/watch?v=6kr9wxSr9-g",
            "How to do Velocity/Time Remapping" : "https://www.youtube.com/watch?v=eo-0tMDzZxI",
            "How to do Shakes"                  : "https://www.youtube.com/watch?v=5hIWruZvboY",
            "How to do Screen Pumps"            : "https://www.youtube.com/watch?v=jqFdqeesKyU"
        }
        experienced = {
            "How to do ZDEPTH Maps"               : "https://www.youtube.com/watch?v=YXaAXfaLaHs",
            "How to do True Motion Blur"          : "https://www.youtube.com/watch?v=o50HiHGN4ss",
            "How to do Perfect Motion blur"       : "https://www.youtube.com/watch?v=gdZrA6fFFiY",
            "What every BCC Effect Does"          : "https://www.youtube.com/watch?v=Kf7xN7Fij-4",
            "What every Saphire Effect does"      : "https://www.youtube.com/watch?v=Wo6z3LT9S-Q",
            "Handy Seamless Transition (Presets)" : "https://www.youtube.com/watch?v=FqIJ0wU2d_A",
            "3 Popular Transitions in AE"         : "https://www.youtube.com/watch?v=0refWK_eIgo"
        }
        embed = get_tutorial_embed(beginners, moderate, experienced, "VFX Tutorials")
        return await ctx.send(embed=embed)



