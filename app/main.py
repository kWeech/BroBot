import discord
from discord.ext import commands
from discord import app_commands

from drafter_cog import drafter_cog
from music_cog import music_cog
from open_ai_cog import open_ai_cog

from dotenv import load_dotenv
load_dotenv()
import os

client = commands.Bot(command_prefix = '.', intents=discord.Intents.all())


@client.event
async def on_ready():
  print("starting up")
  try:
    await client.add_cog(drafter_cog(client))
    await client.add_cog(music_cog(client))  
    # await client.add_cog(open_ai_cog(client))  

    synced = await client.tree.sync()
    print("syncing")
    print("# of synced commands: ", len(synced))
  except Exception as e:
    print(e)

client.run(os.environ["DISCORD_BOT_TOKEN"])