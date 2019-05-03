import re 
import asyncio
import discord
import urllib3
import json
from bs4 import BeautifulSoup

COMMAND = "createevent"
EVENT = r"(https://knightconnect\.campuslabs\.com/engage/event/)(?P<event_id>\d+)"
COMMAND_CHANNEL = 'officer-business'
COMMAND_PATTERN = r"^!{0} {1}$".format(
    COMMAND,
    EVENT
)

async def command_signup(client, message):
    """ Take a KnightConnect event as input and creates a facebook
        event, and prepares Knightroko to make discord announcements
        for it"""
    command_match = re.match(COMMAND_PATTERN, message.content)

    # Throw an error message if the command syntax is wrong.
    if command_match is None:
        response = "You've got the signup syntax wrong. Type !createevent followed by the" +\
                   "Knight Connect event url"
        await message.channel.send(response)

        return

    # Only allow events to be created inside the officer-business channel
    if (str(message.channel) != COMMAND_CHANNEL):
        await message.channel.send("You are unable to do that. To make an event, you " +\
                                   "must be an officer and use that command in #officer-business")
        await message.channel.send("It should have been done in " +  str(message.channel) + " but was done in " + COMMAND_CHANNEL)
        return

    await message.channel.send("Test success!")
    return