import discord
import re 
import asyncio
import discord
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

COMMAND = "signin"
SIGN_IN_SHEET = "Anime Spot Sign-In"
ROSTER_SHEET = 'Signin Roster'
API_FILE = 'data/Knightroko-d23f10bfb24f.json'

async def command_signin(client, message):
    """Signs in a member to a meeting sheet, or allows for a officer to
        start a signin"""


    user_id = message.author.id

    info = await get_details(user_id)

    if info == None:
        await message.channel.send("I could not find your details " + str(message.author.mention))
        await message.channel.send("Be sure that you've first used the <!signup First Last Email> command to register with me!")
        return
    await insert_signin(info)
    await message.channel.send("You have been signed in " + info[2] + "!")
    
async def insert_signin(data):
    """Given a cell from the signin roster, adds the member to the signin sheet"""

    dt = datetime.now().strftime("%m/%d/%Y %H:%M%S")
    new_row = [dt, data[2] + " " + data[3], data[4]]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_FILE, scope)
    gc = gspread.authorize(credentials)

    sheet = gc.open(SIGN_IN_SHEET).sheet1
    sheet.insert_row(new_row,2)
    return

async def get_details(user_id):
    """Takes in a user_id from the discord and returns the sign-in details for 
    that member. If they are not in the roster, return None"""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_FILE, scope)
    gc = gspread.authorize(credentials)

    sheet = gc.open(ROSTER_SHEET).sheet1

    info = sheet.findall(str(user_id))

    # It's possible they may have signed up twice, so we're going to grab their first entry
    if len(info) == 0:
        return None
    else:
        data = sheet.row_values(info[0].row)
        print(data)
        return data
