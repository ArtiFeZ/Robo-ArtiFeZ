from main import main_color, ArtiFeZGuildIconUrl
from .MainEmbed import qEmbed
import discord

def get_tutorial_embed(beginners: dict, moderate: dict, experienced: dict, title: str):
    e = qEmbed(title=title)
    # e.set_footer(text="Robo-ArtiFeZ", icon_url="https://cdn.discordapp.com/avatars/773087870222467113/f1b7c44b37bb8a059800c81da8b79d7b.webp?size=1024")
    e.add_field(
        name="For Beginners or Newbies",
        value=f"\n".join(f"• [{k}]({v})" for k, v in beginners.items()),
        inline=False
    )
    e.add_field(
        name="For Partially Experienced",
        value=f"\n".join(f"• [{k}]({v})" for k, v in moderate.items()),
        inline=False
    )
    e.add_field(
        name="For Experienced",
        value=f"\n".join(f"• [{k}]({v})" for k, v in experienced.items()),
        inline=False
    )
    # e.set_thumbnail(url=ArtiFeZGuildIconUrl)
    e.add_field(name="How does this work?",
                value="• You can simply click on any of the videos above to redirect to te actual video on youtube!\n"
                      "• If you still any help regarding anything, you can head over to the respective channels (<#765054240443596841> or <#765053215162892309>).",
                inline=False)
    e.add_field(name="Please Note:",
                value="• These videos are anyhow **not promoted** by ArtiFeZ or SCYTES Esports in any way.\n"
                      "• These videos are the top results when searched for **FX tutorials** on youtube.",
                inline=False)
    return e