import aiohttp
import json
import os
import discord
from discord.ext import commands
from discord.ui import View, Button

def load_local_paints():
    path = os.path.join("data", "paints.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        print("LOCAL PAINTS RAW:", raw)  # Debug
        if isinstance(raw, dict) and "payload" in raw:
            paints = raw["payload"]
        elif isinstance(raw, list):
            paints = raw
        else:
            paints = []
        print("LOCAL PAINTS FINAL:", paints[:5])  # Debug
        return paints
    except Exception as e:
        print("Error loading paints.json:", e)
        return []

class PaintListView(View):
    def __init__(self, paint_names, ctx):
        super().__init__(timeout=120)
        self.paint_names = paint_names
        self.ctx = ctx
        self.page = 0
        self.per_page = 10
        self.max_page = (len(paint_names) - 1) // self.per_page

    def get_page_content(self):
        start = self.page * self.per_page
        end = start + self.per_page
        page_items = self.paint_names[start:end]
        description = "\n".join(f"- {name}" for name in page_items)
        embed = discord.Embed(
            title="Citadel Paints",
            description=description,
            color=0x3498DB
        )
        embed.set_footer(text=f"Page {self.page + 1} of {self.max_page + 1}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        button.disabled = self.page == 0
        self.next_button.disabled = self.page == self.max_page
        embed = self.get_page_content()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.max_page:
            self.page += 1
        button.disabled = self.page == self.max_page
        self.prev_button.disabled = self.page == 0
        embed = self.get_page_content()
        await interaction.response.edit_message(embed=embed, view=self)


class PaintCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addpaint")
    async def add_paint(self, ctx, *, paint_name):
        data = self.bot.load_inventory()
        paint_name = paint_name.strip()
        if paint_name not in data["paints"]:
            data["paints"].append(paint_name)
            self.bot.save_inventory(data)
            embed = discord.Embed(title="Paint Added", description=f"**{paint_name}** was added to your inventory.", color=0x1ABC9C)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Duplicate Paint", description=f"**{paint_name}** is already in your inventory.", color=0xE74C3C)
            await ctx.send(embed=embed)

    @commands.command(name="removepaint")
    async def remove_paint(self, ctx, *, paint_name):
        data = self.bot.load_inventory()
        paint_name = paint_name.strip()
        if paint_name in data["paints"]:
            data["paints"].remove(paint_name)
            self.bot.save_inventory(data)
            embed = discord.Embed(title="Paint Removed", description=f"**{paint_name}** was removed from your inventory.", color=0xE67E22)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Paint Not Found", description=f"**{paint_name}** was not found in your inventory.", color=0xE74C3C)
            await ctx.send(embed=embed)

    @commands.command(name="mypaints")
    async def my_paints(self, ctx):
        data = self.bot.load_inventory()
        if not data["paints"]:
            embed = discord.Embed(title="Your Paint Inventory", description="Your inventory is empty.", color=0xF1C40F)
            await ctx.send(embed=embed)
        else:
            paint_list = "\n".join(f"- {p}" for p in data["paints"])
            embed = discord.Embed(title="Your Paint Inventory", description=paint_list, color=0x3498DB)
            await ctx.send(embed=embed)

    @commands.command(name="addproject")
    async def add_project(self, ctx, *, project_name):
        data = self.bot.load_inventory()
        project_name = project_name.strip()
        if project_name not in data["projects"]:
            data["projects"].append(project_name)
            self.bot.save_inventory(data)
            embed = discord.Embed(title="Project Added", description=f"Project **{project_name}** was added to your open projects.", color=0x1ABC9C)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Duplicate Project", description=f"Project **{project_name}** is already in your projects list.", color=0xE74C3C)
            await ctx.send(embed=embed)

    @commands.command(name="removeproject")
    async def remove_project(self, ctx, *, project_name):
        data = self.bot.load_inventory()
        project_name = project_name.strip()
        if project_name in data["projects"]:
            data["projects"].remove(project_name)
            self.bot.save_inventory(data)
            embed = discord.Embed(title="Project Removed", description=f"Project **{project_name}** was removed from your projects.", color=0xE67E22)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Project Not Found", description=f"Project **{project_name}** was not found in your projects list.", color=0xE74C3C)
            await ctx.send(embed=embed)

    @commands.command(name="projects")
    async def my_projects(self, ctx):
        data = self.bot.load_inventory()
        if not data["projects"]:
            embed = discord.Embed(title="Your Projects", description="You have no open projects.", color=0xF1C40F)
            await ctx.send(embed=embed)
        else:
            projects_list = "\n".join(f"- {p}" for p in data["projects"])
            embed = discord.Embed(title="Your Open Projects", description=projects_list, color=0x3498DB)
            await ctx.send(embed=embed)

    @commands.command(name="paint")
    async def paint_info(self, ctx, *, paint_name):
        url = "https://citadel-paints-api.onrender.com/paints?name=" + paint_name.replace(" ", "%20")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                    except Exception:
                        data = None
                else:
                    data = None
                print("PAINT API RAW:", data)
                if data and isinstance(data, list) and data:
                    paint = data[0]
                    embed = discord.Embed(title=paint.get('name','Unknown'),
                                          description=f"Type: {paint.get('type', 'Unknown')}\nGroup: {paint.get('colorGroup', 'Unknown')}",
                                          color=0x9B59B6)
                    await ctx.send(embed=embed)
                    return
        local_paints = load_local_paints()
        result = None
        for paint in local_paints:
            if paint_name.lower() == paint.get("name", "").lower():
                result = paint
                break
        if result:
            embed = discord.Embed(title=result.get('name','Unknown'),
                                  description=f"Type: {result.get('type', 'Unknown')}\nGroup: {result.get('colorGroup', 'Unknown')}",
                                  color=0x9B59B6)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Paint Not Found",
                                  description=f"Paint '{paint_name}' not found in the API or local file.",
                                  color=0xE74C3C)
            await ctx.send(embed=embed)

    @commands.command(name="allpaints")
    async def all_paints(self, ctx):
        url = "https://citadel-paints-api.onrender.com/paints"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        paints = await response.json()
                    except Exception:
                        paints = None
                else:
                    paints = None
                print("PAINT API RAW:", paints)
                if paints and isinstance(paints, list):
                    paint_names = [paint['name'] for paint in paints if isinstance(paint, dict) and 'name' in paint]
                else:
                    local_paints = load_local_paints()
                    paint_names = [paint['name'] for paint in local_paints if 'name' in paint]

        if not paint_names:
            embed = discord.Embed(title="Error", description="Could not retrieve paint list.", color=0xE74C3C)
            await ctx.send(embed=embed)
            return

        view = PaintListView(paint_names, ctx)
        embed = view.get_page_content()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(PaintCommands(bot))
