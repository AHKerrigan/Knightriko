from pymongo import MongoClient
import discord
import re

import random
from plugins.Knightrocards.kc_utils import create_card

COMMAND = "summ"

async def command_summ(client, message):

    client = MongoClient()
    db = client['Knightrocards']

    print(db['Characters'].find({"Stars" : 1}).count())
    character = db['Characters'].aggregate([
        {"$sample" : {"size" : 1}}
    ])
    for item in character:
        character = item
    
    await message.channel.send("Commencing Summoning", embed=create_card(character["ID"]))

