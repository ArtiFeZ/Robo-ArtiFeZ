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
            "Adobe Photoshop for Beginners".title() : "https://youtu.be/pFyOznL9UvA",
            "How to make thumbnails".title() : "https://youtu.be/k8B4urrTtxQ",
            "How To Make Thumbnails by Videro \\😎".title() : "https://youtu.be/e-_DAvnMNDo",
            "How to make an easy esports banner".title() : "https://youtu.be/8Nl9RX4Yu7E",
            "How to make a stream package".title() : "https://youtu.be/l_Ddn7h8tDM",
            "How to do Photo manipulation".title() : "https://youtu.be/4hdWChhovvg"
        }
        moderate = {
            "How to make 3D text in Cinema 4D".title() : "https://youtu.be/XmNDi109ECw",
            "How to design emotes".title(): "https://youtu.be/cv80MVC4-tI",
            "How to create Gradient Highlight Mesh Effect".title() : "https://youtu.be/3jiBBesNcB0",
            "How to create fluid abstract background".title() : "https://youtu.be/lG4-03pDFw8",
            "How to create liquid marbelling effects".title() : "https://youtu.be/ouviTuZUB4E",
            "Advanced photo manipulation".title() : "https://youtu.be/XnzGFtUevts",
            "Easy dual lighting effect".title() : "https://youtu.be/Osgt7LP0720",
            "Master Curves in Photoshop".title() : "https://youtu.be/Bvyiydd2dMc",
        }
        experienced = {
            "Not added yet" : "https://www.youtube.com/"
        }
        embed = get_tutorial_embed(beginners, moderate, experienced, "GFX Tutorials")
        return await ctx.send(embed=embed)

    @gfx.command(name="packs", help="Gives a list of some popular gfx packs.", aliases=['pack', 'p'])
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def _gfx_packs(self, ctx: commands.Context, pc_mob : str = None) -> discord.Message:
        if not pc_mob:
            packs: dict = {
                "Glitch Pack - BEST GFX PACK FREE - ANDROID & PC FREE PACK | Abstract GFX PACK 2020\nBy Greck x Lennox" : "https://www.youtube.com/watch?v=79Y8wjUEIjs",
                "GFX PACK! #1 (ANDROID + IOS + PC)\nBy NaoriChan•恋人" : "https://www.youtube.com/watch?v=5vPG2mZtW88",
                "More soon" : "https://www.youtube.com/",
                "a": "",
                "b": "",
                "c": "",
                "d": "",
                "e": "",
                "f": "",
                "g": "",
            }
            e = get_packs_embed(packs, "GFX Packs (Both 💻 and 📱)")
            return await ctx.send(embed=e)
        if pc_mob:
            if "p" in pc_mob.lower():
                packs : dict = {
                    "Not added yet" : "https://www.youtube.com/"
                }
                e = get_packs_embed(packs, "GFX Packs (Only 💻)")
                return await ctx.send(embed=e)
            elif "m" in pc_mob.lower():
                packs: dict = {
                    "Not added yet" : "https://www.youtube.com/"
                }
                e = get_packs_embed(packs, "GFX Packs (Only 📱)")
                return await ctx.send(embed=e)
            else:
                packs: dict = {
                    "Not added yet" : "https://www.youtube.com/"
                }
                e = get_packs_embed(packs, "GFX Packs (Both 💻 and 📱)")
                return await ctx.send(embed=e)