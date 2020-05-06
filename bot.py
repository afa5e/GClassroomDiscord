# bot.py
import os, discord
from dotenv import load_dotenv

#Get tokens from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Removes either the username or discord tag.
detagger = lambda a:str(a)[:-5]
denamer = lambda a:str(a)[-5:]

#Reads the contents of the user lists on startup.
f = open('admins.txt', 'r')
admins = list(map(lambda a:a.rstrip(),f))   #Iterates through all lines in the file and strips newline chars from the end.
f.close()
f = open('discriminatedUsers.txt', 'r')
muted = list(map(lambda a:a.rstrip(),f))
f.close()

bot_state = 'on'

client = discord.Client()

@client.event
async def on_ready():
    print('Online', end='\n\n')

@client.event
async def on_typing(channel, user, when):
    #Check if the user currently typing is the bot to prevent recursion
    if user == client.user:
        return

    if denamer(user) in muted:
        await channel.send(f'{user.mention} please refrain from typing.')
        await user.send('Please refrain from typing.')
        print(f'{user} started typing and was warned', end='\n\n')

@client.event
async def on_message(message):
    global bot_state
    message_author_tag = denamer(message.author)
    if message_author_tag != '#3842' and bot_state == 'on':      #User #3842 is the bot.
        if message_author_tag in muted:
            await message.delete()
            print(f'\"{message}\" from {message.author} was deleted.', end='\n\n')
            await message.author.send('Please cease the actions of sending messages')
    elif message_author_tag in admins:
        print(message.contents, end='\n\n')
        if '~stop' in message.content:
            bot_state = 'off'
            print(f'Bot has been turned off by {message.author}')
            await message.channel.send(f'Bot has been turned off by {message.author}')
        elif '~start':
            bot_state = 'on'
            print(f'Bot has been turned on by {message.author}')
            await message.channel.send(f'Bot has been turned on by {message.author}')
client.run(TOKEN)
