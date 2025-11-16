# Use a specific version of the Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install FFmpeg and dependencies for Deno
RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Deno (recommended for yt-dlp EJS)
RUN curl -fsSL https://deno.land/install.sh | sh \
    && mv /root/.deno/bin/deno /usr/local/bin/deno

# Copy the src directory and requirements.txt into the container
COPY app/ /app/
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run main.py when the container launches
CMD ["python", "main.py"]
