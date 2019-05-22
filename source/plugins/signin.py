import discord

COMMAND = "signin"

async def command_signin(client, message):
    """Signs in a member to a meeting sheet, or allows for a officer to
        start a signin"""

    await message.channel.send("There is not currently an event to sign-in to!")