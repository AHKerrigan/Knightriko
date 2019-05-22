import discord
import re
import os
import json
import feedparser
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

COMMAND = "nextevent"
EVENTS_URL = "https://knightconnect.campuslabs.com/engage/organization/animespot/events"
KC_URL = 'https://knightconnect.campuslabs.com/'
RSS_URL = 'https://knightconnect.campuslabs.com/engage/organization/animespot/events.rss'
#GECKO_PATH = "/home/animespotucf"

async def command_nextevent(client, message):
    """ Displays information on the next Anime Spot meeting"""

    event_information = await rss_scrape(client, message)

    # The Knight Connect RSS feed only shows the next week worth of events
    # In the case where the next meetings is more than a week away, we have 
    # to directly scrape Knight Connect
    if event_information == None:
        await message.channel.send("The next meeting or event is over a week away, this will take a second...")
        event_information = await kc_scrape()
    
    
    response = "Here is the next Anime Spot event!"
    embedded_message = await build_embed(event_information)
    print(embedded_message)
    await message.channel.send(response, embed=embedded_message)

async def rss_scrape(client, message):
    "Parses the Knight Connect RSS feed"

    feed = feedparser.parse(RSS_URL)

    # Unfortunately the RSS feed is only for a week in the future, so in the case where theres
    # more than a week until the next event, we won't get  
    if len(feed['entries']) == 0:
        return None
    
    event_information = {}
    event_information['Name'] = feed['entries'][0]['title']
    event_information['Location'] = feed['entries'][0]['location']

    start = datetime.strptime(feed['entries'][0]['start'], '%a, %d %B %Y %H:%M:%S %Z')
    end = datetime.strptime(feed['entries'][0]['end'], '%a, %d %B %Y %H:%M:%S %Z')

    event_information['Date'] = start.strftime("%B %d, %Y")
    event_information['Time'] = start.strftime("%I:%M%p") + " - " + end.strftime("%I:%M%p")

    # Description is a json, so parse it like one and remove the html junk
    des_soup = BeautifulSoup(feed['entries'][0]['summary_detail']['value'])
    new_des = des_soup.find_all('div', {'class':'p-description description'})[0]
    event_information['Description'] = re.sub('<[^<]+?>', '', new_des.text)

    return event_information
    
async def kc_scrape():
    """ Directly scrapes knight connect for Anime Spot's event list"""
    
    # Dryscrape opens a headless browser because Knight Connect will not load 
    # any information about our events until AFTER the javascript has loaded
    options = Options()
    options.headless = True
    response = webdriver.Firefox(options=options)
    response.get(EVENTS_URL)
    soup = BeautifulSoup(response.page_source, features='lxml')
    events = soup.find_all('a', {'href':re.compile('/engage/event/', re.IGNORECASE)})

    # We only needed the event lists so we can close this afterwards
    response.quit()

    # If event this is empty, then there are no planned events on knight connect
    if len(events) == 0:
        return None

    url = KC_URL + events[0]['href']
    page = urlopen(url)
    soup = BeautifulSoup(page)

    # This line unfortunately took manual inspection of the Knight Connect source
    # It's very likely this may change in the future
    data = json.loads(soup.find_all('script')[2].get_text()[25:-1])

    event_information = {}
    event_information['Name'] = data['preFetchedData']['event']['name']
    event_information['Location'] = data['preFetchedData']['event']['address']['name']

    start_date = datetime.strptime(data['preFetchedData']['event']['startsOn'][:19], '%Y-%m-%dT%H:%M:%S')
    end_date = datetime.strptime(data['preFetchedData']['event']['endsOn'][:19], '%Y-%m-%dT%H:%M:%S')

    event_information['Date'] = start_date.strftime("%B %d, %Y")
    event_information['Time'] = start_date.strftime("%I:%M%p") + " - " + end_date.strftime("%I:%M%p")

    # BS doesn't always remove HTML junk, so we need to process description one more time
    new_des = re.sub('<[^<]+?>', '', data['preFetchedData']['event']['description'])
    new_des = os.linesep.join([s for s in new_des.splitlines() if s])
    event_information['Description'] = new_des

    return event_information

async def build_embed(event_information):
    """ Given a dictionary of event information, created an embedded table
    of that event information"""

    embedded_message = discord.Embed(color=0xffee05)

    embedded_message.add_field(
        name="Event Name",
        value = event_information['Name'],
        inline=False
    )

    embedded_message.add_field(
        name="Date",
        value = event_information['Date'],
        inline=False
    )

    embedded_message.add_field(
        name="Time",
        value = event_information['Time'],
        inline=False
    )

    embedded_message.add_field(
        name="Location",
        value = event_information['Location'],
        inline=False
    )

    embedded_message.add_field(
        name="Description",
        value = event_information['Description'],
        inline=False
    )

    return embedded_message

