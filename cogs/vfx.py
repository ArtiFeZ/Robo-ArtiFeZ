import discord
from discord.ext import commands
from main import main_color, ArtiFeZGuildIconUrl
from utils.tutorialEmbed import get_tutorial_embed
from utils.packsEmbed import get_packs_embed

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

    @vfx.command(name="packs", help="Gives a list of some major vfx packs.", aliases=['pack', 'p'])
    @commands.guild_only()
    async def _vfx_packs(self, ctx : commands.Context):
          packs : dict = {
              "Mega Vfx Pack 2020 - Green Screens, Transitions, Animated Backgrounds, Synthwave Backgrounds & More!" : "https://www.youtube.com/watch?v=muJ204vRkZo",
              "MEGA VFX TRANSITIONS, OVERLAY, ELEMENTS, BACKGROUNDS PACK FOR ANDROID (KINEMASTER, POWER DIRECTOR)" : "https://www.youtube.com/watch?v=pqUzsrV1gkA",
              "VFX Pack 2020 || Android/iOS || Free Download || Visual Effects Pack" : "https://www.youtube.com/watch?v=Q2UkOPlkEl4",
              "200+ Free Overlays HUGE PACK 2020 FOR EDITING (Sony Vegas, After Effects, Premiere Pro etc)" : "https://www.youtube.com/watch?v=okrmWX_V0WE",
              "BEST EDITING PACK [PACK VFX] 🎬" : "https://www.youtube.com/watch?v=9pLHWsQRUW4",
              "Free Pro's 30K Ultimate Preset Pack | Sony Vegas (DO NOT MISS THIS!)" : "https://www.youtube.com/watch?v=29W1GsvEzAI",
              "Motion VFX Pack Vol 2 | Filmora Effect" : "https://www.youtube.com/watch?v=BNeHhp5uu6w",
              "VFX PACK || Free VFX Pack Giveaway || Akash Official" : "https://www.youtube.com/watch?v=vmvejDaufT8",
              "VFX PACK | OVERLAY PACK | PARTICLES PACK | LIGHT | SMOKE | ANIMATED OVERLAY VFX PACK" : "https://www.youtube.com/watch?v=pMwxnPb4XV8",
              "(20K) FREE VFX Editing Pack | 200+ Video Elements, SFX, Fonts & LUTs - Vegas Pro / After Effects" : "https://www.youtube.com/watch?v=OTf7-iAFSD0",
              "Vfx Pack - Big-Vfx - Started Pack" : "https://www.youtube.com/watch?v=2zoJY6_mFsE",
              "The MOTION Pack || After effects || VFX GURU" : "https://www.youtube.com/watch?v=_W_pLPd5I8A",
              "FREE VFX ASSETS - ELECTRICAL FX PACK" : "https://www.youtube.com/watch?v=IsjXlkQEM2U"
          }
          e = get_packs_embed(packs, "VFX Packs")
          return await ctx.send(embed=e)




