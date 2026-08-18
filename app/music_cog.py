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
            # YouTube currently rejects direct audio from its default
            # android_vr client. The Android client's combined format 18
            # remains playable; FFmpeg discards its video stream below.
            'format': '18/bestaudio/best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                },
            },
            'noplaylist': False,
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': False,
            'js_runtimes': {
                'deno': {},
                'node': {},
            },
        }
        self.playlist_ydl_opts = {
            **self.ydl_opts,
            'extract_flat': 'in_playlist',
        }
        self.track_ydl_opts = {
            **self.ydl_opts,
            'extract_flat': False,
            'noplaylist': True,
        }

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -bufsize 512k'
        }

        self.vc = None
        
    def _entry_to_song(self, entry):
        if not entry:
            return None

        title = entry.get('title') or 'Unknown Title'
        source = entry.get('webpage_url') or entry.get('original_url')
        if not source:
            video_id = entry.get('id') or entry.get('url')
            if isinstance(video_id, str) and video_id:
                source = f"https://www.youtube.com/watch?v={video_id}"

        if not source:
            return None

        return {'source': source, 'title': title}

    def _blocking_search_yt(self, item):
        if "list=" in item:
            with YoutubeDL(self.playlist_ydl_opts) as ydl:
                info = ydl.extract_info(item, download=False)

            playlist = []
            for entry in info.get('entries', []):
                song = self._entry_to_song(entry)
                if song:
                    playlist.append(song)
                    print(f"Added {song['title']} to the queue")
            return playlist

        with YoutubeDL(self.track_ydl_opts) as ydl:
            if item.startswith(("http://", "https://")):
                info = ydl.extract_info(item, download=False)
                song = self._entry_to_song(info)
                return [song] if song else []

            info = ydl.extract_info(f"ytsearch:{item}", download=False)
            entries = info.get('entries') or []
            if not entries:
                return []

            song = self._entry_to_song(entries[0])
            return [song] if song else []

    def _blocking_resolve_stream(self, song):
        with YoutubeDL(self.track_ydl_opts) as ydl:
            info = ydl.extract_info(song['source'], download=False)

        if not info:
            raise RuntimeError(f"Could not load audio for {song['title']}")

        stream_url = info.get('url')
        if not stream_url:
            requested_formats = info.get('requested_formats') or []
            for fmt in requested_formats:
                if fmt and fmt.get('url'):
                    stream_url = fmt['url']
                    break

        if not stream_url:
            raise RuntimeError(f"No playable stream found for {song['title']}")

        return stream_url

    def _requeue_song_front(self, song, voice_channel):
        self.music_queue.insert(0, [song, voice_channel])

        
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

    def _after_song(self, error):
        if error:
            print(f"Playback error: {error}")

        future = asyncio.run_coroutine_threadsafe(self.play_music(), self.bot.loop)

        def _log_future_result(task):
            exc = task.exception()
            if exc:
                print(f"Error while starting the next song: {exc}")

        future.add_done_callback(_log_future_result)

    async def play_next(self):
        await self.play_music()

    # infinite loop checking 
    async def play_music(self, interaction: discord.Interaction | None = None):
        if len(self.music_queue) > 0:
            self.is_playing = True
            song, voice_channel = self.music_queue.pop(0)

            #try to connect to voice channel if you are not already connected
            try:
                if self.vc == None or not self.vc.is_connected():
                    self.vc = await voice_channel.connect()

                    #in case we fail to connect
                    if self.vc == None or not self.vc.is_connected():
                        self._requeue_song_front(song, voice_channel)
                        if interaction is not None:
                            await interaction.followup.send("Could not connect to the voice channel.")
                        self.is_playing = False
                        return
                else:
                    await self.vc.move_to(voice_channel)
            except Exception as e:
                print(f"Voice connection error: {e}")
                self._requeue_song_front(song, voice_channel)
                if interaction is not None:
                    await interaction.followup.send("Voice connection failed before playback started.")
                self.is_playing = False
                return

            # Only resolve the stream when the song is about to play.
            loop = asyncio.get_running_loop()
            try:
                m_url = await loop.run_in_executor(None, self._blocking_resolve_stream, song)
            except Exception as e:
                print(f"Error loading stream for {song['title']}: {e}")
                if interaction is not None:
                    await interaction.followup.send(f"Could not load **{song['title']}**. Skipping it.")
                await self.play_music(interaction)
                return

            if self.vc == None or not self.vc.is_connected():
                self._requeue_song_front(song, voice_channel)
                if interaction is not None:
                    await interaction.followup.send("Lost the voice connection before playback started.")
                self.is_playing = False
                return

            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=self._after_song)
            except discord.ClientException as e:
                print(f"Playback start error: {e}")
                self._requeue_song_front(song, voice_channel)
                if interaction is not None:
                    await interaction.followup.send("Connected to voice, but playback could not start.")
                self.is_playing = False
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
            await self.play_music(interaction)
        
    @app_commands.command(name="play")
    @app_commands.describe(query='The song you want to play', play_next='Set to True to play this song next', shuffle='Set to True to shuffle the playlist')
    async def play(self, interaction: discord.Interaction, query: str, play_next: bool = False, shuffle: bool = False):
        # Defer immediately to avoid timeout (within 3 seconds)
        await interaction.response.defer()
        
        if interaction.user.voice is None:
            await interaction.followup.send("Connect to a voice channel!")
            return
        voice_channel = interaction.user.voice.channel

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