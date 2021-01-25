import discord
from discord.ext import commands
from utils.MainEmbed import qEmbed
from utils.readabletime import getReadableTimeBetween
from main import main_color, CommunityRoleID, chatChannelId, ArtiFeZGuildIconUrl, modLogsChannelId, AboutUs
import datetime, random, asyncio

def setup(bot):
    bot.add_cog(welcome(bot))

class welcome(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        # x = {'footer': {'text': 'React with the emoji to get the role!', 'icon_url': 'https://cdn.discordapp.com/icons/715126942294343700/a_4f8b163f2b8a7c7e5ad1263ed2ed699e.gif?size=1024%27%7D', 'fields': [{'name': 'Interest\U0001fa84', 'value': ':art: - GFX Designer\n:movie_camera: - VFX Editor\n:musical_note: - SFX Producer', 'inline': True}, {'name': 'Platform :gear:', 'value': ':computer: - PC/Laptop\n:mobile_phone: - Mobile/Tablet', 'inline': True}, {'name': 'Opinions :thinking:', 'value': ':paintbrush: - GFX Opinions\n:projector: - VFX Opinions', 'inline': True}, {'name': 'Competitions :trophy:', 'value': ':gfxcomp: - GFX Competitions\n:vfxcomp:  - VFX Competitions', 'inline': True}], 'color': 3201788, 'type': 'rich', 'description': 'React with the appropriate emoji to get yourself the role you reacted with!', 'title': 'Reaction Roles!'}

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        await member.add_roles(discord.Object(CommunityRoleID))
        channel = self.bot.get_channel(chatChannelId)
        time = getReadableTimeBetween(member.created_at.timestamp(), datetime.datetime.utcnow().timestamp())
        time_split = time.split(",")
        e = qEmbed(title="New Member!")
        e.description = f"• **Name**: {member.mention}\n" \
                        f"• **Account Created**: {time_split[0] + ' and ' + time_split[1]} ago.\n" \
                        f"• **Lucky Number**: {random.randint(1, 10)} <a:afzparty_blob:783393007075459133>"
        e.set_author(name=str(member), icon_url=member.avatar_url)
        await channel.send(embed=e)
        e2 = qEmbed(title='***Welcome to ArtiFeZ!***', color=main_color,
                    url='https://top.gg/servers/715126942294343700')
        e2.description = AboutUs
        e2.add_field(name="What We Offer",
                     value="""・Frequent Editing Competitions with **Cash Prizes**!
・**Active** Community!
・**Level Based** and **Color** Roles!
・Special **Server Booster Perks**!
・Many people who give opinions on your work!
・A platform to share your work and **get recognized** in the community!""",
                     inline=False)
        e2.add_field(name="Quick start",
                     value="""
・**Reply with one of the following options to have info regarding the same.**
・:one: - I want something made by someone \💵
・:two: - I want to offer/sell my services to others \🌻
・:three: - I want suggestions on my work \🤔
・:four: - I need technical help with my design/software \⚙️
・:five: - I want to showcase my work to the community \👀
・:six: - Let us know instead, contact staff \💁🏻‍♂️
・:seven: - I am here just to chill \😎
        """)
        try:
            tries = 7
            try:
                init = await member.send(embed=e2, content=member.mention)
            except:
                return
            def check(m : discord.Message):
                return m.author == member and m.channel == init.channel and m.content.startswith(tuple([str(x) for x in range(1,8)]))
            while tries > 0:
                msg : discord.Message = await self.bot.wait_for('message', check=check)
                if '1' in msg.content:
                    tries -= 1
                    e1 = qEmbed(title='\😅***Not quite there yet..***', url='https://top.gg/servers/715126942294343700')
                    e1.description = "・The commission system is currently **under development**.\n" \
                                     "・The buyers will be able to **buy services** from the **verified sellers** of ArtiFeZ.\n" \
                                     "・There is no ETA as of now, but it will be out **before 15th December 2020**.\n" \
                                     f"・You can still **reply with another number** ( {tries} attempts left )"
                    await init.channel.send(embed=e1)
                elif '2' in msg.content:
                    tries -= 1
                    e2 = qEmbed(title='\😅***Not quite there yet..***', url='https://top.gg/servers/715126942294343700')
                    e2.description = "・The commission system is currently **under development**.\n" \
                                     "・The buyers will be able to **buy services** from the **verified sellers** of ArtiFeZ.\n" \
                                     "・There is no ETA as of now, but it will be out **before 15th December 2020**.\n" \
                                     f"・You can still **reply with another number** ( {tries} attempts left )"
                    await init.channel.send(embed=e2)
                    continue
                elif '3' in msg.content:
                    tries -= 1
                    e3 = qEmbed(title="\💁🏻‍♂️***Sure Thing!***", url='https://top.gg/servers/715126942294343700')
                    e3.add_field(
                        name='If you are a GFX Designer:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎨 emoji to get the <@&716245903203106816> role.\n"
                              "・You can also react with 🖌 to get the <@&769919914060021770> role. [Optional]\n"
                              "・Now, you can head over to <#765052924073082911> and share your work.\n"
                              "・If you took the <@&769919914060021770> role, you can ping the same role as well afterwards.\n"
                              "・And, that's pretty much it!",
                        inline=False
                    )
                    e3.add_field(
                        name='If you are a VFX Editor:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎥 emoji to get the <@&716246064306323577> role.\n"
                              "・You can also react with 📽 to get the <@&769920213453504514> role. (Optional)\n"
                              "・Now, you can head over to <#765054200647254016> and share your work.\n"
                              "・If you took the <@&769920213453504514> role, you can ping the same role as well afterwards.\n"
                              "・And, that's pretty much it!",
                        inline=False
                    )
                    e3.add_field(
                        name='If you are a SFX Producer:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎵 emoji to get the <@&716246158087028736> role.\n"
                              "・Now, you can head over to <#769955894456221696> and share your work.\n"
                              "・And, that's pretty much it!",
                        inline=False
                    )
                    e3.add_field(name= 'Anything Else?',
                                 value= f'You can still reply with any other number. ( {tries} attempts left )',
                                 inline=False)
                    await init.channel.send(embed=e3)
                    continue
                elif '4' in msg.content:
                    tries -= 1
                    e4 = qEmbed(title="\💁🏻‍♂️***Leave it to us!***", url='https://top.gg/servers/715126942294343700')
                    e4.add_field(
                        name='If you need help in GFX:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎨 emoji to get the <@&716246064306323577> role.\n"
                              "・Now, you can head over to <#765054240443596841> and ask for help.\n"
                              "・Please be patient after asking for help.\n"
                              "・Although we try our best to assist everyone, its not guaranteed that you will be assisted.\n"
                              "・And, that's about it!",
                        inline=False
                    )
                    e4.add_field(
                        name='If you need help in VFX:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎥 emoji to get the <@&716245903203106816> role.\n"
                              "・Now, you can head over to <#765053215162892309> and ask for help.\n"
                              "・Please be patient after asking for help.\n"
                              "・Although we try our best to assist everyone, its not guaranteed that you will be assisted.\n"
                              "・And, that's about it!",
                        inline=False
                    )
                    e4.add_field(
                        name='If you need help in SFX:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎵 emoji to get the <@&716246158087028736> role.\n"
                              "・Now, you can head over to <#769955894087516160> and ask for help.\n"
                              "・Please be patient after asking for help.\n"
                              "・Although we try our best to assist everyone, its not guaranteed that you will be assisted.\n"
                              "・And, that's about it!",
                        inline=False
                    )
                    e4.add_field(name='Anything Else?',
                                 value=f'You can still reply with any other number. ( {tries} attempts left )',
                                 inline=False)
                    await init.channel.send(embed=e4)
                    continue
                elif '5' in msg.content:
                    tries -= 1
                    e5 = qEmbed(title="\💫***Gotcha!***", url='https://top.gg/servers/715126942294343700')
                    e5.add_field(
                        name='If you are a GFX Designer:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎨 emoji to get the <@&716245903203106816> role.\n"
                              "・Now, you can head over to <#765052924073082911> and start sharing your work!\n"
                              "・And, that's about it!",
                        inline=False
                    )
                    e5.add_field(
                        name='If you are a VFX Editor:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎥 emoji to get the <@&716246064306323577> role.\n"
                              "・Now, you can head over to <#765054200647254016> and start sharing your work!\n"
                              "・And, that's about it!",
                        inline=False
                    )
                    e5.add_field(
                        name='If you are a SFX Producer:',
                        value="・Head over to <#715205304303747142> and go to [this message](https://discordapp.com/channels/715126942294343700/715205304303747142/769925228896976896).\n"
                              "・On the message, [react](https://discordapp.fandom.com/wiki/Reactions#:~:text=To%20react%2C%20users%20must%20mouse,emojis%20present%20in%20the%20menu.) with the 🎵 emoji to get the <@&716246158087028736> role.\n"
                              "・Now, you can head over to <#769955894456221696> and share your work.\n"
                              "・And, that's pretty much it!",
                        inline=False
                    )
                    e5.add_field(name='Anything Else?',
                                 value=f'You can still reply with any other number. ( {tries} attempts left )',
                                 inline=False)
                    await init.channel.send(embed=e5)
                    continue
                elif '6' in msg.content:
                    tries -= 1
                    e6 = qEmbed(title="\📨 ***Hello There!***", url="https://top.gg/servers/715126942294343700")
                    e6.add_field(
                        name="More Help",
                        value=f"・You can head over to either <#715851273571794965> or <#765059841890320394> and tag the <@&765531157721776148>.\n"
                              f"・Glad you are here! \🥂"
                    )
                    e6.add_field(name='Anything Else?',
                                 value=f'You can still reply with any other number. ( {tries} attempts left )',
                                 inline=False)
                    await init.channel.send(embed=e6)
                    continue
                elif '7' in msg.content:
                    tries -= 1
                    e7 = qEmbed(title="\💁🏻‍♂️ ***Alright then!***", url="https://top.gg/servers/715126942294343700")
                    e7.description = "・Sure thing, we hope you have a great time here in ArtiFeZ!\n" \
                                     "・Great to have you here! \🥂"
                    e7.add_field(name='Anything Else?',
                                 value=f'You can still reply with any other number. ( {tries} attempts left )',
                                 inline=False)
                    await init.channel.send(embed=e7)
                    continue
                else:
                    tries -= 1
                    await init.channel.send(f"`{msg.content if len(msg.content) <= 1750 else 'A really long message'}` is not an valid option! ( {tries} attempts left )")
                    continue
            await init.channel.send("You have used all your attempts. If you still have any questions, you can head over to <#765059841890320394> and tag the <@&765531157721776148>.")
        except Exception as e:
            if isinstance(e, asyncio.TimeoutError):
                await member.send('You did not reply in time.')
            else:
                videro = self.bot.get_user(331084188268756993)
                await videro.send(f'Welcome System Error:\n'
                                  f'```py\n{e}\n```')
                await member.send(f'I ran into an error! The developer has been informed.\n'
                                  f'Error :\n'
                                  f'```\n{e}\n```')
                raise e

    @commands.Cog.listener()
    async def on_member_remove(self, member : discord.Member):
        time = getReadableTimeBetween(member.joined_at.timestamp(), datetime.datetime.utcnow().timestamp())
        time_split = time.split(",")
        try:
            e2 = qEmbed(title="\😥***Sad to see you go***", url='https://top.gg/servers/715126942294343700', description=f'・Thanks for being in our server for {time_split[0]+" and"+time_split[1]}.\n'
                                                                        f'・If incase you change your mind, here is the invite link \🥺\n'
                                                                        f'・https://www.discord.gg/nT7kQe6jUE')
            await member.send(member.mention, embed=e2)
        except:
            pass
        channel = self.bot.get_channel(modLogsChannelId)

        e = discord.Embed(title="Member Left", color=main_color)
        e.description = f"• **Name**: {member.mention}\n" \
                        f"• **Joined at**: {time_split[0] + ' and' + time_split[1]} ago.\n" \
                        f"• **Roles ({len(member.roles[1:])})**: {', '.join(x.mention for x in member.roles[1:])}"
        e.set_author(name=str(member), icon_url=member.avatar_url)
        e.set_footer(text=self.bot.user.name, icon_url=ArtiFeZGuildIconUrl)
        return await channel.send(embed=e)