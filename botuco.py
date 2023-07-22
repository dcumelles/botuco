import discord
import random
import pyjokes
from yt_dlp import YoutubeDL
import asyncio
import os
from collections import deque
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = discord.Client(intents=discord.Intents.all())

# create a deque to store the songs in the queue
songs_queue = deque()

@bot.event
async def on_ready():
    print('Hello {0.user} !'.format(bot))
    await bot.change_presence(activity=discord.Game('ekisde'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!escoge'):
        args = message.content[8:]
        options = args.split(',')
        choice = random.choice(options)
        await message.channel.send(choice)

    elif message.content.startswith('botuco pa que se saca la pistola?'):
        await message.channel.send("la pistola se saca pa disparar el que la saca panseñal·la es un parguela")

    elif 'xD' in message.content or 'jaja' in message.content:
        await message.channel.send('te rie??¿!?')

    elif message.content.startswith('!chiste'):
        joke = pyjokes.get_joke(language='es', category='all')
        await message.channel.send(joke)
        
    elif message.content.startswith('gilipollas'):
        await message.channel.send("tu puta madre")

    elif message.content.startswith('!play'):
        if message.content.startswith('!playeame'):
            if not message.guild.voice_client is not None:
                try:
                    channel = message.author.voice.channel
                    await channel.connect()
                except discord.errors.ClientException:
                    pass
            else:
                voice_client = message.guild.voice_client
                if voice_client.is_playing():
                    voice_client.stop()
            voice_client = message.guild.voice_client
            source = discord.FFmpegPCMAudio("song.mp3")
            voice_client.play(source)
        url = message.content[6:]
        if not url:
            await message.channel.send("Tete pero donde esta el link?")
            return
        if not url.startswith("https:"):
            await message.channel.send("Solo funciono con linkukos <:poyae:690195426787328004>")
            return

        songs_queue.append(url)
        if not message.guild.voice_client is not None:
            try:
                channel = message.author.voice.channel
                await channel.connect()
                await play_music(message)
            except discord.errors.ClientException:
                pass
        else:
            await play_music(message)

    elif message.content.startswith('!skip'):
        if message.guild.voice_client is not None:
            voice_client = message.guild.voice_client
            if voice_client.is_playing():
                voice_client.stop()
            await play_music(message)
        await message.channel.send("skipeame esta")

    elif message.content.startswith('!stop'):
        if message.guild.voice_client is not None:
            voice_client = message.guild.voice_client
            if voice_client.is_playing():
                voice_client.stop()
            await voice_client.disconnect()
        await message.channel.send("nos vemoooos... chochito😘")
        songs_queue.clear()

    elif message.content.startswith('!alig'):
        if not message.guild.voice_client is not None:
            try:
                channel = message.author.voice.channel
                await channel.connect()
            except discord.errors.ClientException:
                pass
        else:
            voice_client = message.guild.voice_client
            if voice_client.is_playing():
                voice_client.stop()
        voice_client = message.guild.voice_client
        source = discord.FFmpegPCMAudio("alig.mp3")
        voice_client.play(source)

    elif message.content.startswith('!vitas'):
        if not message.guild.voice_client is not None:
            try:
                channel = message.author.voice.channel
                await channel.connect()
            except discord.errors.ClientException:
                pass
        else:
            voice_client = message.guild.voice_client
            if voice_client.is_playing():
                voice_client.stop()
        voice_client = message.guild.voice_client
        source = discord.FFmpegPCMAudio("vitas.mp3")
        voice_client.play(source)


async def play_music(message):
    if not songs_queue:
        return
    url = songs_queue.popleft()

    ydl_opts = {
        'debug':
        True,
        'format':
        'bestaudio/best',
        'outtmpl':
        'song',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        if os.path.exists('song.mp3'):
            os.remove('song.mp3')
        success = False
        while not success:
            try:
                #info = ydl.extract_info(url, download=True)
                #filename = ydl.prepare_filename(info)
                ydl.download(url)
                voice_client = message.guild.voice_client
                source = discord.FFmpegPCMAudio('song.mp3')
                voice_client.play(source)
            except:
                success = False
                continue
            success = True

    # wait for the song to finish playing
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # play the next song in the queue
    await play_music(message)

if __name__ == "__main__":
    bot.run(API_TOKEN)
