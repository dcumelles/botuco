from yt_dlp import YoutubeDL  
import os

url = "https://www.youtube.com/watch?v=S-_UYzYpY7U&ab_channel=JovaniTV"
ydl_opts = {
        'debug':
        True,
        'format':
        'bestaudio/best',
        'outtmpl':
        'cansisong',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

with YoutubeDL(ydl_opts) as ydl:

    success = False
    while not success:
        try:
            #info = ydl.extract_info(url, download=True)
            #filename = ydl.prepare_filename(info)
            ydl.download(url)

        except:
            success = False
            continue
        success = True

