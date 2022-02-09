import email
from webbrowser import get
import re

from imapclient import IMAPClient

HOST = "mail.cs-georgetown.net"
USERNAME = "honeypot"
PASSWORD = "2nyMugpCadfNpUOo"

emails = ["micah003.1", "micah004.1", "micah005", "micah006", "micah009", "micah007", "micah008", "micah0010", "micah011", "micah012", "micah012", "micah013", "micah014", "micah014-1", "micah015", "micah016", "micah017", "micah017-1", "micah018", "micah019", "micah020", "micah021", "micah022", "micah023", "micah024",
          "micah025", "micah025-1", "micah026-1", "micah027", "micah028", "micah028-1", "micah029", "micah029", "micah031", "micah032", "micah033", "micah034", "micah035", "micah036", "micah037", "micah038", "micah039", "micah040", "micah041", "micah042", "micah043", "micah0431", "micah0431-1", "micah044", "micah045"]
services = ["Spotify", "Netflix", "archiveofourown", "Fandom", "Fandom", "IMDb", "IMDb", "Realtor.com", "Zillow", "Redfin", "Redfin", "rightmove", "DocuSign", "DocuSign", "Jehovah's Witnesses", "Jehovah's Witnesses", "findagrave", "findagrave", "Badoo", "Badoo", "BibleGateway", "YouVersion", "YouVersion", "Zoom",
            "Zoom", "Reddit", "Reddit", "Twitter", "Twitter", "LinkedIn", "LinkedIn", "Microsoft", "Microsoft", "Amazon", "Amazon", "eBay", "Rakuten", "AliExpress", "AliExpress", "Walmart", "CoinMarketCap", "CoinMarketCap", "eToro", "Binance", "Binance", "MarketWatch", "foxbusiness", "foxbusiness", "CoinGecko", "CoinGecko"]

with IMAPClient(HOST) as client:
    # Initial login and email count
    client.login(USERNAME, PASSWORD)
    select_info = client.select_folder('INBOX')
    print('%d messages in INBOX' % select_info[b'EXISTS'])

    # Scope settings
    messages = client.search("ALL")
    # Search through all emails in Inbox, by individual message
    for uid, message_data in client.fetch(messages, "RFC822").items():
        email_message = email.message_from_bytes(message_data[b"RFC822"])
        counter = 0
        violationCounter = 0
        # Parsing for our email address
        to = email_message.get("To")
        location = to.find('<') + 1
        if(to.find('<') != -1):
            to = to[location:to.find('@')]
        else:
            to = to[0:to.find('@')]
        # Sort through to find matching email address, check to make sure service is expected service
        for address in emails:
            if(address is to):
                if(services[counter] not in email_message.get("From")):
                    violationCounter += 1
                    print("Violation: " + str(uid) + ",  " + email_message.get("From") + ", " + email_message.get(
                        "Subject") + ", " + email_message.get("To") + " at " + email_message['date'] + ", should be " + services[counter] + " to " + address)
            counter += 1
    print(str(violationCounter) + " Violations")
    client.logout()
    b'Logging out'