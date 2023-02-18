# import yt_dlp

# URLS = ['https://www.youtube.com/watch?v=MZV0CIFQbbE']

# ydl_opts = {
#     'format': 'm4a/bestaudio/best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }]
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     source = ydl.download(URLS)

# import yt_dlp

# ydl_opts = {
#     'format': 'bestaudio/best',
#     'quiet': True,
#     'outtmpl': '%(id)s.%(ext)s', # use id and extension of the video as the output filename
#     'noplaylist': True, # don't download entire playlist
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3', # convert to mp3 if possible
#         'preferredquality': '320', # target bitrate in kbps
#     }],
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info('https://www.youtube.com/watch?v=5YF60E1l014', download=False)
#     audio_url = info_dict['url']

# print(f"The direct URL of the audio file is: {audio_url}")
import os
os.environ["OPENAI_API_KEY"] = "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"
print(os.environ["OPENAI_API_KEY"])