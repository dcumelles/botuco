import random
import pyjokes
from discord import Message
from song_ops import download_song, play_file, search_youtube


async def handle_message(message: Message):
    msg_command = message.content.split()[0]
    msg_args = message.content[len(msg_command)+1:]
    if msg_command in command_map:
        await command_map[msg_command](message, msg_args)
    return


async def handle_escoge(message: Message, msg_args: str):
    options = msg_args.split(',')
    choice = random.choice(options)
    await message.channel.send(choice)


async def handle_chiste(message: Message):
    joke = pyjokes.get_joke(language='es', category='all')
    await message.channel.send(joke)


async def handle_play(message: Message, msg_args: str):
    url = msg_args
    if not url:
        await message.channel.send("Tete pero donde esta el link?")
        return
    if not url.startswith("https:"):
        await message.channel.send("Solo funciono con linkukos <:poyae:690195426787328004>")
        return
    success = await download_song(url)
    if success:
        await play_file(message)
    else:
        await message.channel.send("ha petao tete")


async def handle_busca(message: Message, msg_args: str):
    if not msg_args:
        await message.channel.send("Tete pero que busco?")
        return
    url = await search_youtube(message, msg_args)
    await handle_play(message, url)


async def handle_stop(message: Message):
    if message.guild.voice_client is not None:
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        await voice_client.disconnect()
    await message.channel.send("nos vemoooos... chochito😘")

async def handle_halloween(message: Message):
    await play_file(message, "halloween.mp3")


async def handle_skippy(message: Message):
    await play_file(message, "skippy.mp3")


async def handle_lostios(message: Message):
    await play_file(message, "lostios.mp3")


async def handle_alig(message: Message):
    await play_file(message, "alig.mp3")


async def handle_vitas(message: Message):
    await play_file(message, "vitas.mp3")


command_map = {
    '!escoge': handle_escoge,
    '!chiste': handle_chiste,
    '!play': handle_play,
    '!busca': handle_busca,
    '!stop': handle_stop,
    '!halloween': handle_halloween,
    '!skippy': handle_skippy,
    '!lostios': handle_lostios,
    '!alig': handle_alig,
    '!vitas': handle_vitas
}
