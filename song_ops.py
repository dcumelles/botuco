import os
from yt_dlp import YoutubeDL
import discord
from dotenv import load_dotenv
import requests
from io import BytesIO

load_dotenv()
YOUTUBE_API_KEY=os.getenv('YOUTUBE_API_KEY')

async def download_song(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        if os.path.exists('song.mp3'):
            os.remove('song.mp3')
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading song: {e}")
            return False
    return True


async def play_file(message: discord.Message, file = "song.mp3"):
    if not message.guild.voice_client is not None:
        try:
            channel = message.author.voice.channel
            await channel.connect()
        except discord.errors.ClientException:
            pass
    message.guild.voice_client.play(discord.FFmpegPCMAudio(file))


async def search_youtube(message: discord.Message, query):
    url = f"https://www.googleapis.com/youtube/v3/search?q={query}&type=video&part=snippet&key={YOUTUBE_API_KEY}"
    response = requests.get(url=url).json()
    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    await message.channel.send(f"He encontrao esto: {response['items'][0]['snippet']['title']}")
    response = requests.get(response['items'][0]['snippet']['thumbnails']['default']['url'])
    await message.channel.send(file=discord.File(BytesIO(response.content), filename='thumbnail.png'))
    return video_url
