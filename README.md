# Citadel-color

This Discord bot helps you track your Citadel paint collection and open projects.  
It supports adding, removing, and listing paints and projects, plus paint info lookup using a community API.

## Features

- Log your Citadel paints and projects
- List your paints and projects
- Lookup basic paint details by name
- Store inventory in a `data/Inventory.json` file
- Securely manage your bot token with a `.env` file

## Setup

1. Clone or download the repo  
2. Create a `.env` file with your Discord bot token: `DISCORD_TOKEN=your_bot_token_here`
3. Install dependencies:

```cmd
pip install -r requirements.txt
```

4. Run the bot:

```cmd
python main.py
```

## Commands

All commands use the prefix `!`. Example: `!addpaint Mephiston Red`

- `!addpaint [paint name]`  
  Add a Citadel paint color to your inventory.

- `!removepaint [paint name]`  
  Remove a paint color from your inventory.

- `!mypaints`  
  List all the paint colors currently in your inventory.

- `!addproject [project name]`  
  Add an open project to your project list.

- `!removeproject [project name]`  
  Remove a project from your open project list.

- `!projects`  
  List all your open projects.

- `!paint [paint name]`  
  Look up information about a specific Citadel paint from the community API.

- `!allpaints`  
  Display a list of all available Citadel paints (shows up to the first 50 to avoid flooding).

