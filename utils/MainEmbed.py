import discord
from main import *

class qEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.from_dict(dict(**kwargs))
        self.set_footer(text="Robo-ArtiFeZ・Developed with 💖 by Videro#9999", icon_url=ArtiFeZGuildIconUrl)
        self.color = main_color

    def __str__(self):
        return self

    def __len__(self):
        return len(self.fields)

