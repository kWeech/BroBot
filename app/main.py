import discord
from discord.ext import commands
from discord import app_commands

from drafter_cog import drafter_cog
from music_cog import music_cog


client = commands.Bot(command_prefix = '.', intents=discord.Intents.all())


@client.event
async def on_ready():
  print("starting up")
  try:
    await client.add_cog(drafter_cog(client))
    await client.add_cog(music_cog(client))  
    synced = await client.tree.sync()
    print("syncing")
    print("# of synced commands: ", len(synced))
  except Exception as e:
    print(e)

client.run("MTA3MTU0Njc2OTE5Mzg0NDgzNw.GCrRBs.0JgAt5xA-y0Gb_n9eeEooAiZMon2EJ-6tMdbCw")