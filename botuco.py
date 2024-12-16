import discord
import os
from dotenv import load_dotenv
from messages import handle_message
from discord import Message

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Hello {0.user} !'.format(bot))
    await bot.change_presence(activity=discord.Game('ekisde'))


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    await handle_message(message)


if __name__ == "__main__":
    bot.run(API_TOKEN)
