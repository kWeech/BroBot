import discord
from discord.ext import commands
from discord import app_commands
import random

class drafter_cog(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.armello_list = ["Thane, the Winter Wolf", "Amber, the Far Seeker", "Mercurio, the Grinning Blade", "Sana, the Forest Sister", "River, the Howling Arrow", "Barnaby, the Screwloose", "Zosha, the Whirlwind", "Brun, the Oakbreaker", "Magna, the Unbroken", "Elyssia, Wardress of Warrens", "Sargon, the Death Teller", "Ghor, the Wyldkin", "Horace, the Iron Poet", "Scarlet, the Bandit King", "Sylas, the Fisher of Souls", "Twiss, the Little Lightpaw", "Hargrave, the Thunder Earl", "Griotte, the Butcher Baroness", "Fang, the Exiled", "Yordana, the Devourer", "Agniya, the Revenant", "Nazar, the Maniac", "Oxana, the Sentinel", "Volodar, the Wormchanter"]
    
    self.civ_list = ["Akkad", "Aksum", "America", "Arabia", "Argentina", "Armenia", "Assyria", "Australia", "Austria", "Ayyubids", "Aztec", "Babylon", "Belgium", "Boers", "Bolivia", "Brazil", "Brunei", "Bulgaria", "Burma", "Byzantium", "Canada", "Carthage", "Celts", "Chile", "China", "Colombia", "Cuba", "Denmark", "Egypt", "England", "Ethiopia", "Finland", "France", "Franks", "Gaul", "Georgia", "Germany", "Golden Horde", "Goths", "Greece", "Hittites", "Hungary", "Huns", "Inca", "India", "Ireland", "Indonesia", "Iroquois", "Israel", "Italy", "Japan", "Jerusalem", "Khmer", "Kilwa", "Kongo", "Korea", "Lithuania", "Macedonian", "Madagascar", "Manchuria", "Maori", "Maurya", "Maya", "Mexican", "Mongolia", "Moors", "Morocco", "Mysore", "Netherlands", "New Zealand", "Nabatea", "Normandy", "Norway", "Nubia", "Oman", "Ottomans", "Palmyra", "Persia", "Philippines", "Phoenician", "Poland", "Polynesia", "Portugal", "Prussian", "Romania", "Rome", "Russia", "Scotland", "Shoshone", "Siam", "Sioux", "Songhai", "Spain", "Sumeria", "Sweden", "Switzerland", "Tibet", "Timurids", "Tonga", "Turkey", "Ukraine", "UAE", "Vatican", "Venetian", "Vietnam", "Wales", "Yugoslavia", "Zimbabwe", "Zulu"]

    self.ng_list = ["Stag - Eikthyrnir", "Goat - Heidrun", "Wolf - Fenrir", "Raven - Huginn and Muninn", "Bear - Bjarki", "Boar - Slidrugtanni", "Snake - Sváfnir", "Dragon - Nidhogg", "Horse - Svadilfari", "Kraken - Lyngbakr", "Ox - Himminbrjotir", "Lynx - Brundr and Kaelinn", "Squirrel - Ratatoskr", "Rat - Dodsvagr", "Eagle - Hræsvelg", "Lion - Neustria"]

  def drafter(self, draft_list, num_players, num_choices=3):
    random_list = random.sample(draft_list, num_players*num_choices)
    chunk_size = len(random_list) // num_players
    return [random_list[i:i+chunk_size] for i in range(0, len(random_list), chunk_size)]

  @app_commands.command(name = "draft", description="test")
  @app_commands.choices(game=[app_commands.Choice(name="Civ", value="civ"), app_commands.Choice(name="Armello", value="armello"), app_commands.Choice(name="Northgard", value="ng")])
  async def draft(self, interaction: discord.Interaction, game: app_commands.Choice[str], num_players: int, num_choices: int):
    if game.value == "civ":
      res = self.drafter(self.civ_list, num_players, num_choices)
    elif game.value == "armello":
      res = self.drafter(self.armello_list, num_players, num_choices)
    elif game.value == "ng":
      res = self.drafter(self.ng_list, num_players, num_choices)
    count = 1
    str_out = "Game: " + game.name + " | Players: " + str(num_players) + " | Choices: " + str(num_choices) + "\n\n"
    for item in res:
      str_out += "Player " + str(count) + ": " + str(' | '.join(item)) + "\n"
      count += 1
    await interaction.response.send_message(str_out)

async def setup(client: commands.Bot) -> None:
  await client.add_cog(drafter_cog(client))