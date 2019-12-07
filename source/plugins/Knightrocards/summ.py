import discord
import re

COMMAND = "summ"

async def command_summ(client, message):
    await message.channel.send("Commencing summoning")