"""Main driver script for Knightroko.

This script creates the Discord client interface and provides a hook into
Knightroko's plugins.

Written by Tiger Sachse.
"""
import re
import sys
import signal
import discord
import asyncio
from plugins import COMMANDS, INLINES, FILTERED_CHANNELS

TOKEN_FILE = "data/discord_token.txt"
COMMAND_PATTERN = r"^!(?P<command>[a-zA-Z0-9]+)"

# Create a Discord client to interface with Discord servers.
client = discord.Client()

@client.event
async def on_message(message):
    """Check for commands after each new message."""

    # Skip messages emitted by Knightroko.
    if message.author == client.user:
        return

    # Check if message is in a filtered channel.
    for filtered_channels in FILTERED_CHANNELS.keys():
        if message.channel.name in filtered_channels:
            await FILTERED_CHANNELS[filtered_channels](client, message)

            return

    # Check message for inline commands.
    for inline in INLINES.keys():
        if re.search(inline, message.content):
            await INLINES[inline](client, message)

            return
    if message.content.startswith('bites za dusto'):
        e = discord.Embed()
        e.set_image(url="https://cdn.discordapp.com/attachments/647607970674507791/727599643357085856/image0.gif")
        await message.channel.send("", Embed=e)
        return

    command_match = re.match(COMMAND_PATTERN, message.content, re.IGNORECASE)
    if command_match is not None:
        command = command_match.group("command")
        message.content = message.content.replace(command, command.lower(), 1)
        command = command.lower()

        # If the command is supported, execute its function. Else call
        # the "help" function.
        if command in COMMANDS.keys():
            await COMMANDS[command](client, message)
        else:
            await COMMANDS["help"](client, message)


@client.event
async def on_member_join(member):
	channel = client.get_channel(535609411540877339)
	
	message = "Welcome to the UCF Anime Spot Discord " + member.mention + \
	"! Please state your first name, and how you heard about us." + \
	"Then, you will be given a role and entry into the rest of the server!"
	await asyncio.sleep(2)
	await channel.send(message)


def load_token():
    """Load the Discord API authentication token."""
    with open(TOKEN_FILE, "r") as token_file:
        return token_file.read().strip()


def handle_signals(signal_number, stack_frame):
    """Gracefully shut down the client."""
    client.close()
    sys.exit(0)


# Fire up the bot.
signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)
client.run(load_token())
