# BroBot

BroBot is a Discord bot that drafts picks for games, plays music in voice channels via YouTube, uses openai's APIs to respond to chat messages and create images.

## Commands

### Gaming

- /draft -> drafts random picks for players for Lekmod version of Civ5, Northgard, and Armello

### OpenAI

- /chat -> uses OpenAI's chat NLP ai to respond to prompt
- /image -> uses OpenAI's DALLE to create AI images based on the given prompt

### Music/Audio

- /play -> takes a query, searches it on YouTube and plays the first search result's audio in the voice channel you are in
- /skip -> skips song
- /queue -> shows song queue
- /pause -> pauses music
- /resume -> resumes music
- /clear -> clears queue
- /disconnect -> disconnects bot from voice channel

## Required Libraries

- discord
- FFMPEG
- PyNaCl
- python-dotenv
- openai
- yt_dlp

## Setup

- install required libraries
- install FFMPEG and add it to your path
- setup .env file with personal OPENAI_API_KEY and DISCORD_BOT_TOKEN
- run main.py
