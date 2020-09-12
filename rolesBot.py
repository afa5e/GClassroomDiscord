# bot.py
import os, discord
from dotenv import load_dotenv

#Get tokens from .env
load_dotenv()
TOKEN = 'NzA2Njg4ODU0MTUyOTcwMjcw.Xq95SA.dnjxCPbtGycJgT5lOlzXovL3fLs'
#Removes either the username or discord tag.
detagger = lambda a:str(a)[:-5]
denamer = lambda a:str(a)[-5:]

bot_state = True

client = discord.Client()

@client.event
async def on_ready():
    print('Online', end='\n\n')

@client.event
async def on_message(message):
    global bot_state
    message_author_tag = denamer(message.author)
    if message_author_tag != '#3842' and bot_state:     #User #3842 is the bot.
        print('message received')
        addCommand, removeCommand = '', ''
        msg = message.content.lower()
        addCommand = msg.startswith('add')
        removeCommand = msg.startswith('remove')
        if addCommand:
            role = msg[4:]
            await message.author.send(f'You have joined the `{role}` role.')
            print(f'{message.author} joined the {role} role.')
        elif removeCommand:
            role = msg[7:]
            await message.author.send(f'The `{role}` role has been removed.')
            print(f'{message.author} requested the removal of the role {role}.')
        else:
            print('Message did not qualify.')
client.run(TOKEN)
