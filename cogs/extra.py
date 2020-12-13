import discord
from discord.ext import commands
from main import ShowCaseChannelsID
import re
from utils.MainEmbed import qEmbed


def setup(bot):
    bot.add_cog(Extra(bot))


class Extra(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in ShowCaseChannelsID:
            e = qEmbed(title="**Don't Chat!**",
                       description=f"・<#{message.channel.id}> is a channel strictly to **showcase your {message.channel.name.strip('・showcase-').upper()} work** 😅\n・Chatting here/passing comments is **not allowed** 🙇🏻‍♂️")
            e2 = qEmbed(title="**One at a time!**",
                        description=f"・{message.author.mention}, please showcase your work **one by one**!・This is to ensure that each of your work gets attention and not gets skipped over!")
            if message.author.bot:
                return
            regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url = re.findall(regex, message.clean_content)
            urls = [x[0] for x in url]
            if len(urls) >= 1:
                await message.add_reaction('⭐')
            elif message.attachments:
                if len(message.attachments) == 1:
                    await message.add_reaction('⭐')
                elif len(message.attachments) > 1:
                    try:
                        await message.author.send(embed=e2)
                    except Exception as e:
                        if isinstance(e, discord.Forbidden):
                            await message.channel.send(embed=e, delete_after=10)
            else:
                try:
                    await message.delete()
                    await message.author.send(embed=e)
                except Exception as e:
                    if isinstance(e, discord.Forbidden):
                        await message.channel.send(embed=e, delete_after=10)
                    elif isinstance(e, discord.NotFound):
                        pass
                    else:
                        await message.channel.send(e, delete_after=5)
                        raise e

        else:
            return None
