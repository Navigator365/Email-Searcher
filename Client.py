import email
import gspread
from webbrowser import get

from imapclient import IMAPClient

HOST = "mail.cs-georgetown.net"
USERNAME = "honeypot"
PASSWORD = "2nyMugpCadfNpUOo"
CURRENT_SEARCH = 51

gc = gspread.service_account()
sh = gc.open("Email Signup Website Sheet")

emails = sh.sheet1.get_values('A2:A' + str(CURRENT_SEARCH))
services = sh.sheet1.get_values('G2:G' + str(CURRENT_SEARCH))

finalSheet = gc.open('Email Violations')
finalSheet.share('bensdodge255@gmail.com', perm_type='user', role='writer')


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
            if(address[0] is to):
                if(services[counter][0] not in email_message.get("From")):
                    violationCounter += 1
                    finalSheet.sheet1.append_row([uid, email_message.get("From"), email_message.get(
                        "Subject"), email_message.get("To"), email_message['date']])
                    print("Violation: " + str(uid) + ",  " + email_message.get("From") + ", " + email_message.get(
                        "Subject") + ", " + email_message.get("To") + " at " + email_message['date'] + ", should be " + services[counter][0] + " to " + address[0])
            counter += 1

    print(str(violationCounter) + " Violations")
    client.logout()
    b'Logging out'
