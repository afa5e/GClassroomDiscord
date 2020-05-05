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

@client.event
async def on_message(message):
    message_author_tag = denamer(message.author)
    if message_author_tag != '#3842' and message_author_tag in muted:      #User #3842 is the bot.
            try:
                await message.delete()
                print(f'\"{message}\" deleted.')
            except discord.HTTPException:
                print("HTTP Exception")
            except discord.Forbidden:
                print("Forbidden")
            except discord.NotFound:
                print("Message not found")
            except:
                print('An error occurred during message deletion')

client.run(TOKEN)
