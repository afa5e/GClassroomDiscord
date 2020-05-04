# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_typing(channel, user, when):
    #Check if the user currently typing is the bot to prevent recursion
    if user == client.user:
        return

    #removes the discord user identifier code and preceding delimiter
    detagger = lambda a:str(user)[:-5]
    denamer = lambda a:str(user)[-5:]

    if denamer(user) == "#0206":
        message = 'stop typing'
        username = detagger(user)
        await channel.send(f'{user.mention} stop typing')
        await user.send(message, tts=True)
    else:
        await channel.send(f'{user.mention} continue')

client.run(TOKEN)
