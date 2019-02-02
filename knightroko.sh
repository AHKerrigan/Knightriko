# A small shell script that handles spinning up
# and shutting down the bot.

# Written by Tiger Sachse.

LION_PID="lion_pid_temp.txt"

# Kill the bot.
kill_knightroko() {
    if [ ! -f $LION_PID ]; then
        echo "Knightroko is not running."
    else
        printf "Killing Knightroko (%d)...\n" $(cat $LION_PID)
        kill $(cat $LION_PID)

        rm -rf source/plugins/__pycache__
        rm -f $LION_PID
    fi
}

# Start the bot.
start_knightroko() {
    kill_knightroko

    cd source

    echo "Starting Knightroko..."
    python3 knightroko.py &
    echo $! > ../$LION_PID

    cd ..
}

# Install dependencies.
install_dependencies() {
    if [[ $EUID -ne 0 ]]; then
        echo "This operation must be run as root." 
        exit 1
    fi

    apt install python3-pip
    pip3 install discord BeautifulSoup4 httplib2 pillow

    printf "\n\n========================================================================\n"
    echo "You need the Discord and weather API tokens before the bot will work."
    echo "These are pinned in the #lion_development channel of the UCF CS Discord."
    echo "Ask a moderator for access to this channel."
    printf "========================================================================\n"
}

# Main entry point of the script.
case $1 in
    "--start")
        start_knightroko
        ;;
    "--kill")
        kill_knightroko
        ;;
    "--install-dependencies")
        install_dependencies
        ;;
esac
