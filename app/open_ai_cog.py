# import discord
# from discord.ext import commands
# from discord import app_commands
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # Set the OpenAI API key
# openai.api_key = os.environ["OPENAI_API_KEY"]

# class open_ai_cog(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot

#     async def chat_gpt_api(self, prompt):
#         model_engine = "gpt-3.5-turbo"  # or "gpt-4" if you have access

#         try:
#             response = await openai.ChatCompletion.acreate(
#                 model=model_engine,
#                 messages=[{"role": "user", "content": prompt}],
#                 max_tokens=200,
#             )
#             return response['choices'][0]['message']['content'].strip()
#         except Exception as e:
#             print(f"OpenAI API Error: {e}")
#             return "Sorry, I couldn't process your request."

#     async def image_gpt_api(self, prompt):
#         try:
#             response = await openai.Image.acreate(
#                 prompt=prompt,
#                 n=1,
#                 size="256x256",
#             )
#             url = response['data'][0]['url']
#             return url
#         except Exception as e:
#             print(f"OpenAI API Error: {e}")
#             return None

#     @app_commands.command(name="chat")
#     async def chat(self, interaction: discord.Interaction, text: str):
#         await interaction.response.defer(thinking=True)
#         response_text = await self.chat_gpt_api(text)
#         await interaction.followup.send(f"*{interaction.user.name}: {text}*\n\n{response_text}")

#     @app_commands.command(name="image")
#     async def image(self, interaction: discord.Interaction, text: str):
#         await interaction.response.defer(thinking=True)
#         image_url = await self.image_gpt_api(text)
#         if image_url:
#             embed = discord.Embed(title=f"*{interaction.user.name}: {text}*")
#             embed.set_image(url=image_url)
#             await interaction.followup.send(embed=embed)
#         else:
#             await interaction.followup.send("Sorry, I couldn't generate the image.")
