import discord
from discord.ext import commands
from discord import app_commands
import random

class drafter_cog(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.armello_list = ["Thane, the Winter Wolf", "Amber, the Far Seeker", "Mercurio, the Grinning Blade", "Sana, the Forest Sister", "River, the Howling Arrow", "Barnaby, the Screwloose", "Zosha, the Whirlwind", "Brun, the Oakbreaker", "Magna, the Unbroken", "Elyssia, Wardress of Warrens", "Sargon, the Death Teller", "Ghor, the Wyldkin", "Horace, the Iron Poet", "Scarlet, the Bandit King", "Sylas, the Fisher of Souls", "Twiss, the Little Lightpaw", "Hargrave, the Thunder Earl", "Griotte, the Butcher Baroness", "Fang, the Exiled", "Yordana, the Devourer", "Agniya, the Revenant", "Nazar, the Maniac", "Oxana, the Sentinel", "Volodar, the Wormchanter"]
    
    self.civ_list = ["Akkad - Sargon"
                     , "Aksum - Ezana"
                    , "America - Washington"
                    , "Arabia - Harun al-Rashid"
                    , "Argentina - Eva Perón"
                    , "Armenia - Tiridates III"
                    , "Assyria - Ashurbanipal"
                    , "Australia - Henry Parker"
                    , "Austria - Maria Theresa"
                    , "Ayyubids - Saladin"
                    , "Aztecs - Montezuma"
                    , "Babylon - Nebuchadnezzar II"
                    , "Belgium - Leopold II"
                    , "Boers - Stephanus Johannes Paulus Kruger"
                    , "Bolivia - Tata Belzu"
                    , "Brazil - Pedro II"
                    , "Brunei - Bolkiah"
                    , "Bulgaria - Asparukh Khan"
                    , "Burma - Anawrahta"
                    , "Byzantium - Theodora"
                    , "Canada - John A. MacDonald"
                    , "Carthage - Dido"
                    , "Celts - Boudicca"
                    , "Chile - Bernardo O’ Higgens"
                    , "China - Wu Zetian"
                    , "Colombia - Simon Bolivar"
                    , "Cuba - Fidel Castro"
                    , "Denmark - Harald Bluetooth"
                    , "Egypt - Ramesses II"
                    , "England - Elizabeth"
                    , "Ethiopia - Haile Selassie"
                    , "Finland - Mannerheim"
                    , "France - Napoleon"
                    , "Franks - Charlemagne"
                    , "Gaul - Vercingetorix"
                    , "Georgia - Tamar"
                    , "Germany - Bismarck"
                    , "Golden Horde - Batu Khan"
                    , "Goths - Alaric I"
                    , "Greece - Pericles"
                    , "Hittites - Muwatallis"
                    , "Huns - Attila"
                    , "Hungary - András II"
                    , "Inca - Pachacuti"
                    , "India - Gandhi"
                    , "Indonesia - Gajah Mada"
                    , "Ireland - Michael Collins"
                    , "Iroquois - Hiawatha"
                    , "Israel - David"
                    , "Italy - Vittorio Emanuele III"
                    , "Japan - Oda Nobunaga"
                    , "Jerusalem - Fulk V"
                    , "Khmer - Suryavarman II"
                    , "Kilwa - Ali ibn al-Hassan Shirazi"
                    , "Kongo - Mvemba a Nzinga"
                    , "Korea - Sejong"
                    , "Lithuania - Vytautas"
                    , "Macedonia - Alexander"
                    , "Madagascar (Malagasy) - Ralambo"
                    , "Manchuria - Nurhaci"
                    , "Maori - Te Rauparaha"
                    , "Maurya - Ashoka"
                    , "Maya - Pacal"
                    , "Mexico - Benito Juarez"
                    , "Mongolia - Genghis Khan"
                    , "Moors - Abd-ar-Rahman III"
                    , "Morocco - Ahmad al-Mansur"
                    , "Mysore - Hyder Ali"
                    , "Nabataea - Aretas III"
                    , "Netherlands - William"
                    , "New Zealand - Michael Joseph Savage"
                    , "Normandy - William the Conqueror"
                    , "Norway - Harald Hardrada"
                    , "Nubia - Amanitore"
                    , "Oman - Saif bin Sultan"
                    , "Ottomans - Suleiman"
                    , "Palmyra - Zenobia"
                    , "Papal States (Vatican) - Urban II"
                    , "Persia - Darius I"
                    , "Philippines - Emilio Aguinaldo"
                    , "Phoenicia - Hiram"
                    , "Poland - Casimir III"
                    , "Polynesia - Kamehameha"
                    , "Portugal - Maria I"
                    , "Prussia - Frederick"
                    , "Romania - Carol I"
                    , "Rome - Augustus Caesar"
                    , "Russia - Catherine"
                    , "Scotland - Robert the Bruce"
                    , "Shoshone - Pocatello"
                    , "Siam - Ramkhamhaeng"
                    , "Sioux- Sitting Bull"
                    , "Songhai - Askia"
                    , "Spain - Isabella"
                    , "Sumeria - Gilgamesh"
                    , "Sweden - Gustavus Adolphus"
                    , "Switzerland - Jonas Furrer"
                    , "Tibet - Ngawang Lobsang Gyatso"
                    , "Timurids - Timur"
                    , "Tonga - 'Aho'eitu"
                    , "Turkey - Ataturk"
                    , "United Arab Emirates (UAE) - Sheikh Zayed"
                    , "Ukraine - Yaroslav I"
                    , "Venice - Enrico Dandolo"
                    , "Vietnam - Hai Ba Trung"
                    , "Wales - Owain Glyndwr"
                    , "Yugoslavia - Aleksandar I "
                    , "Zimbabwe - Nyatsimba Mutota"
                    , "Zulu - Shaka"]
    
    print(len(self.civ_list))
    
    self.ng_list = ["Stag - Eikthyrnir", "Goat - Heidrun", "Wolf - Fenrir", "Raven - Huginn and Muninn", "Bear - Bjarki", "Boar - Slidrugtanni", "Snake - Sváfnir", "Dragon - Nidhogg", "Horse - Svadilfari", "Kraken - Lyngbakr", "Ox - Himminbrjotir", "Lynx - Brundr and Kaelinn", "Squirrel - Ratatoskr", "Rat - Dodsvagr", "Eagle - Hræsvelg", "Lion - Neustria", "Stoat - Nominoe"]

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