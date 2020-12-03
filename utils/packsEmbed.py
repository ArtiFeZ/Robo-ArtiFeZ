from main import main_color, ArtiFeZGuildIconUrl
from discord import *
from .MainEmbed import qEmbed

def get_packs_embed(packs : dict, title : str):
    e = qEmbed(title=title)
    # e.set_thumbnail(url=ArtiFeZGuildIconUrl)
    # e.set_footer(text="Robo-ArtifeZ", icon_url=ArtiFeZGuildIconUrl)
    e.description = "\n".join(f'• [Hover For Title `|` Click To Redirect]({v} "{k}")' for k, v in packs.items())
    e.add_field(name="How does this work?",
                value="• You can hover your mouse over the text to see the video respective video title.\n"
                      "• If you're on mobile, click the hover text to see them.\n"
                      "• You can also click on then to go the respective youtube video.\n",
                )
    e.add_field(name="Please Note:",
                value="• These videos are anyhow **not promoted** by ArtiFeZ or SCYTES Esports in any way.\n"
                      "• These videos are the top results when searched for **FX tutorials** on youtube.",
                inline=False)
    return e