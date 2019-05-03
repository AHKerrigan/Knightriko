"""Produce a modest help menu that lists high level commands.

Written by Tiger Sachse.
"""
import discord

COMMAND = "help"

async def command_help_menu(client, message):
    """Display an embedded help menu."""
    response = "Here's a list of commands that I understand..."

    embedded_message = discord.Embed(color=0xffee05)
    embedded_message.add_field(
        name="!info",
        value="Show some more information about Knightroko.",
        inline=False
    )

    embedded_message.add_field(
        name="!users",
        value="Display the latest server membership count.",
        inline=False
    )

    embedded_message.add_field(
        name="!poll time prompt (choice1, choice2, etc)",        
        value="Create a new poll. Time is in minutes.",
        inline=False
    )

    embedded_message.add_field(
        name = "!suggest \"Event Name\" Event description", 
        value= "Add a new event/meeting idea to the suggestion box to be voted on"+\
               " by the club",
        inline=False
    )

    embedded_message.add_field(
        name = "!signup First Last Email", 
        value= "Registers your information so you can sign into events and meets with one command. "+\
               "Don't worry, I'll delete your message so nobody can see your info.",
        inline=False
    )

    embedded_message.add_field(
        name="!garage [garage]",
        value="See the status of the UCF parking garages.",
        inline=False
    )

    embedded_message.add_field(
        name="!listroles",
        value="List all server roles.",
        inline=False
    )

    embedded_message.add_field(
      name="!dog [breed]",
      value="Get a picture of a good boy!",
      inline=False
    )

    embedded_message.add_field(
        name="!sponge message",
        value="Create a spicy, sarcastic meme.",
        inline=False
    )

    await message.channel.send(response, embed=embedded_message)
