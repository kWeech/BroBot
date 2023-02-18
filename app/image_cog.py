import discord
from discord.ext import commands
from discord import app_commands
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


class image_cog(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  def image_gpt_api(self, prompt):

    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
    )
    url = response['data'][0]['url']
    return str(url)
    

  @app_commands.command(name = "image", description="test")
  async def image(self, interaction: discord.Interaction, text: str):
    await interaction.response.defer(thinking = True)
    embed = discord.Embed(title="*" + str(interaction.user.name) + ": " + text + "*")
    embed.set_image(url=self.image_gpt_api(text))

    await interaction.followup.send(embed=embed)

async def setup(client: commands.Bot) -> None:
  await client.add_cog(image_cog(client))