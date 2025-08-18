import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Citadel Bot Help",
            description="Here are all available commands:",
            color=0x2ECC71
        )
        embed.add_field(
            name="🎨 Paint Management",
            value=(
                "`!addpaint <name>` — Add a paint to your inventory\n"
                "`!removepaint <name>` — Remove a paint from your inventory\n"
                "`!mypaints` — View your entire paint inventory"
            ),
            inline=False
        )
        embed.add_field(
            name="🛠️ Project Management",
            value=(
                "`!addproject <name>` — Add a new project\n"
                "`!removeproject <name>` — Remove a project\n"
                "`!projects` — View your open projects"
            ),
            inline=False
        )
        embed.add_field(
            name="🔍 Paint Info & Lists",
            value=(
                "`!paint <name>` — Get info about a specific paint\n"
                "`!allpaints` — View all Citadel paints with navigation"
            ),
            inline=False
        )
        embed.set_footer(text="Tip: Use buttons in !allpaints to paginate the paint list.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
