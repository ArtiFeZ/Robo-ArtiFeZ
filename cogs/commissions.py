import discord, asyncio
from discord.ext import commands
from main import main_color, ApprovedRoleID, ArtiFeZGuildIconUrl
from utils.MainEmbed import qEmbed


def setup(bot):
    bot.add_cog(Commissions(bot))


class Commissions(commands.Cog):
    """
    Commands related to the commission system in ArtiFeZ.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="register", help="Registers you as a seller on the server.", aliases=['re', 'rs'])
    @commands.has_role(ApprovedRoleID)
    @commands.guild_only()
    async def register(self, ctx: commands.Context):
        # todo **New System**
        pass
        # yes_list = ["yes", "y", "yea", "yep"]
        # no_list = ["no", "nah", "n", "nope"]
        # valid_answers = yes_list + no_list
        # qna = [
        #     "Please reply with a **link to your portfolio**.",
        #     "**Since when** are you doing GFX/VFX/SFX?",
        #     "Which **payment methods** do you accept? [Separate different methods by a `,`]",
        #     "What is your **minimum budget**? [Reply with `None` if there is none.]",
        # ]
        # answers = []
        # index = 0
        # try:
        #     init: discord.Message = await ctx.author.send(f"Hello {ctx.author.name}!")
        #
        #     def check(m: discord.Message):
        #         return m.author == ctx.author and m.channel == init.channel
        #
        #     await ctx.message.add_reaction("☑")
        #     await ctx.send(f"📨 {ctx.author.name}, check your DMs.")
        #     for q in qna:
        #         index += 1
        #         e = qEmbed().set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        #         e.description = q + "\n*(You have 3 minutes to reply)*"
        #         await init.channel.send(embed=e)
        #         try:
        #             answer = await self.bot.wait_for('message', check=check, timeout=180)
        #             answers.append(answer.content)
        #             # await init.channel.send(f"**Question {index}**: {q}\n**Answer**: {answer.content}")
        #             await asyncio.sleep(0.3)
        #         except asyncio.TimeoutError:
        #             await init.channel.send("\❌ You did not answer in time.")
        #     videro = await self.bot.fetch_user(331084188268756993)
        #     await videro.send(f'\n'.join(f"{x}. {y}"for x,y in enumerate(answers, 1)))
        # except Exception as e:
        #     if isinstance(e, discord.Forbidden):
        #         e2 = discord.Embed(color=discord.Color.red(), title="Please open your DMs.")
        #         await ctx.send(embed=e2)
        #     else:
        #         await ctx.send(f"Ran into an error:\n```\n{e}\n```Please Contact Videro#9999.")
        #         raise e
