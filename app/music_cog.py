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
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }   
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                # Check if the item is a playlist
                if "list" in item:
                    info = ydl.extract_info(item, download=False)
                    playlist = []
                    for entry in info['entries']:
                        try:
                            # Try extracting information for each video in the playlist
                            video_info = ydl.extract_info(entry['webpage_url'], download=False)
                            playlist.append({'source': video_info['url'], 'title': video_info['title']})
                            print(f"Added {video_info['title']} to the queue")
                        except Exception as e:
                            print(f"Error downloading song from playlist: {e}")
                            continue  # Skip to the next song if there's an error
                    return playlist
                else:
                    # Processing for a single video
                    info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                    return [{'source': info['url'], 'title': info['title']}]
            except Exception as e:
                print(f"Error processing item: {e}")
                return False

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
        songlist = self.search_yt(query)
        if type(songlist) == type(True) or not songlist:
            await interaction.followup.send("Could not download the query. Incorrect format or no songs found.")
            return

        if shuffle:
            random.shuffle(songlist)

        # Add songs to the queue and inform the user
        for song in songlist:
            if play_next:
                self.music_queue.insert(0, [song, voice_channel])
            else:
                self.music_queue.append([song, voice_channel])
            await interaction.followup.send(f"Added {song['title']} to the queue.")

        if not self.is_playing:
            await self.play_music(interaction.response)
    
    # @app_commands.command(name="play")
    # async def play(self, interaction: discord.Interaction, query: str):
    #     await interaction.response.defer(thinking=True)

    #     voice_channel = interaction.user.voice.channel
    #     if voice_channel is None:
    #         await interaction.followup.send("Connect to a voice channel!")
    #     else:
    #         songlist = self.search_yt(query)
    #         if type(songlist) == type(True) or not songlist:
    #             await interaction.followup.send("Could not download the query. Incorrect format or no songs found.")
    #         else:
    #             print(songlist)
    #             print(len(songlist))
    #             for song in songlist:
    #                 self.music_queue.append([song, voice_channel])

    #             if not self.is_playing:
    #                 await self.play_music(interaction.response)
    #             await interaction.followup.send(f"Added {len(songlist)} songs to queue.")
    # @app_commands.command(name="play")
    # @app_commands.describe(query='The song you want to play', play_next='Set to True to play this song next')
    # async def play(self, interaction: discord.Interaction, query: str, play_next: bool = False):
    #     await interaction.response.defer(thinking=True)

    #     voice_channel = interaction.user.voice.channel
    #     if voice_channel is None:
    #         await interaction.followup.send("Connect to a voice channel!")
    #     else:
    #         songlist = self.search_yt(query)
    #         if type(songlist) == type(True) or not songlist:
    #             await interaction.followup.send("Could not download the query. Incorrect format or no songs found.")
    #         else:
    #             if play_next:
    #                 # Insert the songs to play next in the queue
    #                 for song in reversed(songlist):
    #                     self.music_queue.insert(0, [song, voice_channel])
    #                 message = f"Added {len(songlist)} song(s) to play next."
    #             else:
    #                 # Add the songs to the end of the queue
    #                 for song in songlist:
    #                     self.music_queue.append([song, voice_channel])
    #                 message = f"Added {len(songlist)} song(s) to the queue."

    #             if not self.is_playing:
    #                 await self.play_music(interaction.response)
    #             await interaction.followup.send(message)
    @app_commands.command(name="play")
    @app_commands.describe(query='The song you want to play', play_next='Set to True to play this song next', shuffle='Set to True to shuffle the playlist')
    async def play(self, interaction: discord.Interaction, query: str, play_next: bool = False, shuffle: bool = False):
        voice_channel = interaction.user.voice.channel
        if voice_channel is None:
            await interaction.followup.send("Connect to a voice channel!")
            return

        # Respond immediately to avoid timeout
        await interaction.response.send_message("Adding songs to the queue...")

        # Start the asynchronous process of adding songs
        asyncio.create_task(self.async_add_songs(interaction, query, voice_channel, play_next, shuffle))
    
    @app_commands.command(name="pause")
    async def pause(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await interaction.response.send_message("Music paused")
        else:
            await interaction.response.send_message("Nothing is playing")

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
            await self.resume(interaction)
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
        await self.vc.disconnect()
        await interaction.response.send_message("Disconnected")
    
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