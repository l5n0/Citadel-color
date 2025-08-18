import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DATA_DIR = "data"
        INVENTORY_FILE = os.path.join(DATA_DIR, "Inventory.json")
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, "w") as f:
                json.dump({"paints": [], "projects": []}, f, indent=2)
        self.INVENTORY_FILE = INVENTORY_FILE

    def load_inventory(self):
        with open(self.INVENTORY_FILE, "r") as f:
            return json.load(f)

    def save_inventory(self, data):
        with open(self.INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    async def setup_hook(self):
        await self.load_extension("commands.paint_commands")
        await self.load_extension("commands.help_command")

bot = MyBot(command_prefix="!", intents=intents)
bot.remove_command('help')  # Remove the default help command for a custom embedded one

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

if __name__ == "__main__":
    bot.run(TOKEN)
