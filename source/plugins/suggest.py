import re
import asyncio
import discord
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']



COMMAND = "suggest"
GOOGLE_SHEET = 'Anime Spot Suggestion Box (Responses)'
API_FILE = 'data/G_DOCS_API.json'
EVENT_NAME_FORMAT = r"(?P<event_name>\"(.*?)\")"
EVENT_DESCRIPTION_FORMAT = r"(?P<event_description>.+)"
COMMAND_PATTERN = r"^!{0} {1} {2}$".format(
    COMMAND,
    EVENT_NAME_FORMAT,
    EVENT_DESCRIPTION_FORMAT
)

async def command_suggest(client, message):
    """ Takes an event name as well as an event description and saves them
        to the suggestion box sheet"""
    
    command_match = re.match(COMMAND_PATTERN, message.content)

    # Throw an error message if the command syntax is wrong.
    if command_match is None:
        response = "You've got the suggest syntax wrong. Try '!help."
        await message.channel.send(response)
        return

    # Get the event name as well as the description
    # Have to splice a little to get rid of quotes
    event_name = command_match.group("event_name")[1:-1]
    event_description = command_match.group("event_description")

    await save_row(event_name, event_description)

    await message.channel.send("Your suggestion for " + event_name +\
                                " has been added " + message.author.display_name + "!")

async def save_row(event_name, event_description):
    """ Save an event and description to the suggestion box doc"""
   
    # Construct the new row, including the date and time
    new_row = []
    new_row.append(str(datetime.datetime.now()))
    new_row.append(event_name)
    new_row.append(event_description)

    # Authorize the google sheet and open
    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_FILE, scope)
    gc = gspread.authorize(credentials)

    sheet = gc.open(GOOGLE_SHEET).sheet1

    # The new info is inserted at row 2, right below the headers in the sheet
    sheet.insert_row(new_row, 2)


    

