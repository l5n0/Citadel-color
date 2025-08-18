import aiohttp
import json
import os
from discord.ext import commands

def load_local_paints():
    path = os.path.join("data", "paints.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        print("LOCAL PAINTS RAW:", raw)  # Debug: See what's loaded
        # If your file wraps paints in 'payload', extract them
        if isinstance(raw, dict) and "payload" in raw:
            paints = raw["payload"]
        elif isinstance(raw, list):
            paints = raw
        else:
            paints = []
        print("LOCAL PAINTS FINAL:", paints[:5])  # Debug: See first 5 paints
        return paints
    except Exception as e:
        print("Error loading paints.json:", e)
        return []

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
            await ctx.send(f"Added **{paint_name}** to inventory.")
        else:
            await ctx.send(f"**{paint_name}** already in inventory.")

    @commands.command(name="removepaint")
    async def remove_paint(self, ctx, *, paint_name):
        data = self.bot.load_inventory()
        paint_name = paint_name.strip()
        if paint_name in data["paints"]:
            data["paints"].remove(paint_name)
            self.bot.save_inventory(data)
            await ctx.send(f"Removed **{paint_name}** from inventory.")
        else:
            await ctx.send(f"**{paint_name}** not found in inventory.")

    @commands.command(name="mypaints")
    async def my_paints(self, ctx):
        data = self.bot.load_inventory()
        if not data["paints"]:
            await ctx.send("Inventory is empty.")
        else:
            await ctx.send("Current inventory:\n" + "\n".join(f"- {p}" for p in data["paints"]))

    @commands.command(name="addproject")
    async def add_project(self, ctx, *, project_name):
        data = self.bot.load_inventory()
        project_name = project_name.strip()
        if project_name not in data["projects"]:
            data["projects"].append(project_name)
            self.bot.save_inventory(data)
            await ctx.send(f"Added project: **{project_name}**.")
        else:
            await ctx.send(f"Project **{project_name}** already in inventory.")

    @commands.command(name="removeproject")
    async def remove_project(self, ctx, *, project_name):
        data = self.bot.load_inventory()
        project_name = project_name.strip()
        if project_name in data["projects"]:
            data["projects"].remove(project_name)
            self.bot.save_inventory(data)
            await ctx.send(f"Removed project: **{project_name}**.")
        else:
            await ctx.send(f"Project **{project_name}** not found in inventory.")

    @commands.command(name="projects")
    async def my_projects(self, ctx):
        data = self.bot.load_inventory()
        if not data["projects"]:
            await ctx.send("No open projects.")
        else:
            await ctx.send("Open projects:\n" + "\n".join(f"- {p}" for p in data["projects"]))

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
                    msg = (
                        f"**{paint.get('name','Unknown')}**\n"
                        f"Type: {paint.get('type', 'Unknown')} | Group: {paint.get('colorGroup', 'Unknown')}\n"
                    )
                    await ctx.send(msg)
                    return
        local_paints = load_local_paints()
        result = None
        for paint in local_paints:
            if paint_name.lower() == paint.get("name", "").lower():
                result = paint
                break
        if result:
            msg = (
                f"**{result.get('name','Unknown')}**\n"
                f"Type: {result.get('type', 'Unknown')} | Group: {result.get('colorGroup', 'Unknown')}\n"
            )
            await ctx.send(msg)
        else:
            await ctx.send(f"Paint '{paint_name}' not found in the API or local file.")

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
                    max_display = 50
                    paint_names = [paint['name'] for paint in paints if isinstance(paint, dict) and 'name' in paint]
                    display_list = paint_names[:max_display]
                    message = "**Available Citadel Paints (showing first 50):**\n" + "\n".join(display_list)
                    if len(paint_names) > max_display:
                        message += f"\n...and {len(paint_names) - max_display} more."
                    await ctx.send(message)
                    return
        local_paints = load_local_paints()
        if local_paints and isinstance(local_paints, list):
            max_display = 50
            paint_names = [paint['name'] for paint in local_paints if 'name' in paint]
            display_list = paint_names[:max_display]
            message = "**Available Citadel Paints (local, first 50):**\n" + "\n".join(display_list)
            if len(paint_names) > max_display:
                message += f"\n...and {len(paint_names) - max_display} more."
            await ctx.send(message)
        else:
            await ctx.send("Could not retrieve paint list from the API or local file.")

async def setup(bot):
    await bot.add_cog(PaintCommands(bot))
