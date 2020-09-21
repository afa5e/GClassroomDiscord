from __future__ import print_function
import pickle, discord
import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# Original scope, view courses only.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
# Push notifications only
SCOPES = ['https://www.googleapis.com/auth/classroom.push-notifications']
# Discord bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=13).execute()
    courses = results.get('courses', [])

    # Setup the Discord API
    detagger = lambda a:str(a)[:-5]
    denamer = lambda a:str(a)[-5:]
    bot_state = True
    client = discord.Client()

    @client.event
    async def on_message(message):
        if denamer(message.author) == '#6644':
            print(message.channel)
            print('message received')
            if not courses:
                await message.author.send('No courses found.')
            else:
                await message.author.send('Course:')
                for course in courses:
                    if course['courseState'] == "ACTIVE":
                        response = course['name'] + ": " + str(course['alternateLink'])
                        await message.author.send(response)

    @client.event
    async def on_ready():
        print('Online', end='\n\n')

    client.run(TOKEN)

if __name__ == '__main__':
    main()
