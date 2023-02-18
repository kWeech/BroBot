import discord
from discord.ext import commands
from discord import app_commands
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

class chat_cog(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  def chat_gpt_api(self, prompt):
    model_engine = "text-davinci-003" # or any other GPT model

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=200
    )

    return completions.choices[0].text.strip()
    

  @app_commands.command(name = "chat", description="test")
  async def chat(self, interaction: discord.Interaction, text: str):
    await interaction.response.defer(thinking = True)
    await interaction.followup.send("*" + str(interaction.user.name) + ": " + text + "*\n\n" + self.chat_gpt_api(text))

async def setup(client: commands.Bot) -> None:
  await client.add_cog(chat_cog(client))