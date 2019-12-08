from pymongo import MongoClient

import discord

def create_card(char_id):

    client = MongoClient()
    db = client['Knightrocards']
    character = db['Characters'].find({"ID" : char_id})[0]

    card = discord.Embed(title="Series Placeholder", colour=discord.Colour(0xffc904), url="https://discordapp.com", description=":star: " * character['Stars'])

    card.set_image(url=character['Picture'])
    card.set_author(name=character['Name'])
    card.set_footer(text=character['PP'], icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/sparkles_2728.png")

    return card
