import discord
import re

import pandas as pd
from pymongo import MongoClient

from plugins.Knightrocards.kc_init import COMMANDS

COMMAND = "kc"
KC_COMMAND = r"(?P<kc_command>[a-zA-Z ]*)"
KC_CONTENT = r"(?P<kc_content>[a-zA-Z ]*)"
COMMAND_PATTERN = r"^!kc {0} {1}$".format(KC_COMMAND, KC_CONTENT)

DB = "data/knightrocards.db"


async def command_kc(client, message):

    command_match = re.match(COMMAND_PATTERN, message.content)
    command = command_match.group("kc_command")
    content = command_match.group("kc_content")
    if command_match != None:
        await COMMANDS[command](client, message)