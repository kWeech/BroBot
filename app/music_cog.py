from ast import alias
import discord
from discord.ext import commands
from discord import app_commands
from yt_dlp import YoutubeDL
import random
import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'noplaylist': False,
            'ignoreerrors': True,
            'extract_flat': False,  # Ensure full info is extracted
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'playlistend': 50,  # Limit playlist extraction to 50 items
        }

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -bufsize 512k'
        }

        self.vc = None
        
    def _blocking_search_yt(self, item):
        with YoutubeDL(self.ydl_opts) as ydl:
            if "list" in item:
                info = ydl.extract_info(item, download=False)
                playlist = []
                for entry in info['entries']:
                    if entry:  # Ensure entry is not None
                        playlist.append({'source': entry['url'], 'title': entry['title']})
                        print(f"Added {entry['title']} to the queue")
                return playlist
            else:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)
                info = info['entries'][0]
                return [{'source': info['url'], 'title': info['title']}]

        
    async def search_yt(self, item):
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(None, self._blocking_search_yt, item)
            return result
        except Exception as e:
            print(f"Error processing item: {e}")
            return []


    #  #searching the item on youtube
    # def search_yt(self, item):
    #     with YoutubeDL(self.ydl_opts) as ydl:
    #         try:
    #             # Check if the item is a playlist
    #             if "list" in item:
    #                 info = ydl.extract_info(item, download=False)
    #                 playlist = []
    #                 for entry in info['entries']:
    #                     if entry:  # Ensure entry is not None
    #                         playlist.append({'source': entry['url'], 'title': entry['title']})
    #                         print(f"Added {entry['title']} to the queue")
    #                 return playlist
    #             else:
    #                 # Processing for a single video
    #                 info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
    #                 return [{'source': info['url'], 'title': info['title']}]
    #         except Exception as e:
    #             print(f"Error processing item: {e}")
    #             return False

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    async def async_add_songs(self, interaction, query, voice_channel, play_next, shuffle):
        songlist = await self.search_yt(query)
        if type(songlist) == type(True) or not songlist:
            await interaction.followup.send("Could not download the query. Incorrect format or no songs found.")
            return

        if shuffle:
            random.shuffle(songlist)

        # Add songs to the queue and inform the user
        added_songs = []
        for song in songlist:
            if play_next:
                self.music_queue.insert(0, [song, voice_channel])
            else:
                self.music_queue.append([song, voice_channel])
            added_songs.append(song['title'])
            
       # Set a limit on how many song titles to display
        max_display = 10  # Adjust this number as needed
        displayed_songs = added_songs[:max_display]
        songs_list = '\n'.join(displayed_songs)
        total_songs = len(added_songs)

        if total_songs > max_display:
            songs_list += f"\n...and {total_songs - max_display} more songs."

        await interaction.followup.send(f"Added {total_songs} songs to the queue:\n{songs_list}")
        
        if not self.is_playing:
            await self.play_music(interaction.response)
        
    @app_commands.command(name="play")
    @app_commands.describe(query='The song you want to play', play_next='Set to True to play this song next', shuffle='Set to True to shuffle the playlist')
    async def play(self, interaction: discord.Interaction, query: str, play_next: bool = False, shuffle: bool = False):
        # Defer immediately to avoid timeout (within 3 seconds)
        await interaction.response.defer()
        
        voice_channel = interaction.user.voice.channel
        if voice_channel is None:
            await interaction.followup.send("Connect to a voice channel!")
            return

        # Send initial message
        await interaction.followup.send("Adding songs to the queue...")

        # Start the asynchronous process of adding songs
        asyncio.create_task(self.async_add_songs(interaction, query, voice_channel, play_next, shuffle))
    
    @app_commands.command(name="pause")
    async def pause(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await interaction.response.send_message("Music paused")
        elif len(self.music_queue) > 0:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await interaction.response.send_message("Music resumed")
        else:
            await interaction.response.send_message("No song is currently playing")

    @app_commands.command(name="resume")
    async def resume(self, interaction: discord.Interaction):
      if self.is_paused:
        self.is_paused = False
        self.is_playing = True
        self.vc.resume()
        await interaction.response.send_message("Music resumed")

    @app_commands.command(name="skip")
    async def skip(self, interaction: discord.Interaction):
        if self.vc != None and self.vc.is_playing():
            self.vc.stop()
            await interaction.response.send_message("Song skipped")
        else:
            await interaction.response.send_message("No song is currently playing")

    @app_commands.command(name="queue")
    async def queue(self, interaction: discord.Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await interaction.response.send_message(retval)
        else:
            await interaction.response.send_message("No music in queue")

    @app_commands.command(name="clear")
    async def clear(self, interaction: discord.Interaction):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await interaction.response.send_message("Music queue cleared")

    @app_commands.command(name="disconnect")
    async def dc(self, interaction: discord.Interaction):
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        if self.vc != None and self.vc.is_connected():
            await self.vc.disconnect()
            await interaction.response.send_message("Disconnected")
        else:
            await interaction.response.send_message("Not connected to a voice channel")
    
    @app_commands.command(name="shuffle")
    async def shuffle(self, interaction: discord.Interaction):
        # Check if there are songs in the queue
        if not self.music_queue:
            await interaction.response.send_message("The music queue is empty, nothing to shuffle.")
            return

        # Shuffling the music queue
        random.shuffle(self.music_queue)
        
        # Inform the user
        await interaction.response.send_message("Music queue has been shuffled.")