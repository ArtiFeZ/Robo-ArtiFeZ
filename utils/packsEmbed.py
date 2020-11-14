from main import main_color, ArtiFeZGuildIconUrl
from discord import *

def get_packs_embed(packs : dict, title : str):
    e = Embed(title=title, color=main_color)
    e.set_thumbnail(url=ArtiFeZGuildIconUrl)
    e.set_footer(text="Robo-ArtifeZ", icon_url=ArtiFeZGuildIconUrl)
    e.description = "\n".join(f'• [Hover For Title `|` Click To Redirect]({v} "{k}")' for k, v in packs.items())
    e.add_field(name="How does this work?",
                value="You can hover your mouse over the text to see the video respective video title."
                      " If you're on mobile, click the hover text to see them."
                      " You can also click on then to go the respective youtube video. Enjoy!")
    return e