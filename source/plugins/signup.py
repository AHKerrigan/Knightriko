import re
import asyncio
import discord

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']



COMMAND = "signup"
GOOGLE_SHEET = 'Signin Roster'
API_FILE = 'data/Knightroko-d23f10bfb24f.json'
FIRST_NAME = r"(?P<first_name>[a-zA-Z ]*)"
LAST_NAME = r"(?P<last_name>[a-zA-Z ]*)"
EMAIL = r"(?P<email>[^ ]*)"
COMMAND_PATTERN = r"^!{0} {1} {2} {3}$".format(
    COMMAND,
    FIRST_NAME,
    LAST_NAME,
    EMAIL
)

async def command_signup(client, message):
    """Take a first name, last name, and email, and add them
       to the sign-in roster"""

    command_match = re.match(COMMAND_PATTERN, message.content)

    # Deletes the message once it's sent so their email is not public
    await message.delete()

    # Throw an error message if the command syntax is wrong.
    if command_match is None:
        response = "You've got the signup syntax wrong. Try `!help`."
        await message.channel.send(response)

        return
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name('data/' + API_FILE, scope)
    gc = gspread.authorize(credentials)
    
    user_id = message.author.id
    user_name = str(message.author)
    first_name = command_match.group("first_name")
    last_name = command_match.group("last_name")
    email = command_match.group("email")

    new_row = [user_id, user_name, first_name, last_name, email]

    sheet = gc.open(GOOGLE_SHEET).sheet1

    # The new info is inserted at row 2, right below the headers in the sheet
    sheet.insert_row(new_row, 2)
    await message.channel.send("Your info has been added " + first_name + "!")

