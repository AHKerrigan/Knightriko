import discord
import re

import pandas as pd
from pymongo import MongoClient

COMMAND = "kc"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)

DB = "data/knightrocards.db"


async def command_kc(client, message):

    
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)

    client = MongoClient()
    db = client['Knightrocards']
    characters = db['Characters']
    test = {}
    test["Rank"] = str(50)
    test['ID'] = str(32817)
    test['Name'] = "Alec"
    
    characters.insert_one(test)
    print(db.list_collection_names())
    print(characters.find_one({"Rank": "50"}))


    if command_match == None:
        await message.channel.send("No command given " + str(message.author.display_name))
    else:
        await message.channel.send(command_match.group("rest"))