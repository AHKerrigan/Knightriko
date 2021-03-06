"""Initializer for included Knightroko plugins.

This script imports all installed Knightroko plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""

from plugins import (
    dog,
    info,
    poll,
    sponge,
    help_menu,
    user_count,
    garage_status,
    require_links,
    signup,
    signin,
    suggest,
    nextevent,
    kc
)

FILTERED_CHANNELS = {
    require_links.FILTERED_CHANNELS : require_links.filter_require_links
}

COMMANDS = {
    dog.COMMAND : dog.command_dog,
    info.COMMAND : info.command_info,
    poll.COMMAND : poll.command_poll,
    sponge.COMMAND : sponge.command_sponge,
    help_menu.COMMAND : help_menu.command_help_menu,
    user_count.COMMAND : user_count.command_user_count,
    garage_status.COMMAND : garage_status.command_garage_status,
    signup.COMMAND : signup.command_signup,
    suggest.COMMAND : suggest.command_suggest,
    nextevent.COMMAND : nextevent.command_nextevent,
    signin.COMMAND : signin.command_signin,
    kc.COMMAND : kc.command_kc
}

INLINES = {
}
