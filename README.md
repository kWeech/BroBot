## Commands

### Gaming

- /draft

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
- python-dotenv
- yt_dlp

## Setup

- install required libraries
- install FFMPEG and add it to your path
- setup .env file with personal DISCORD_BOT_TOKEN
- run main.py

### Docker

#### Building the Image

```bash
docker build -t brobot .
```

#### Running Options

1. **Basic Docker Run**

```bash
docker run --env-file .env brobot
```

2. **Docker Compose**

```bash
docker-compose up
```

3. **Docker Hub Deployment**

```bash
# Login to Docker Hub
docker login

# Tag your image with your Docker Hub username
docker tag brobot yourusername/brobot

# Push to Docker Hub
docker push yourusername/brobot
```

Note: Make sure your `.env` file is in the same directory as where you run the Docker commands.
