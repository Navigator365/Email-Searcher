import csv
import gspread
import time
import urllib.request
from websitecategorization import *
import xml.etree.ElementTree as ET


# For official use, use Full Site Ranking
sheet_name = "bigtest"

gc = gspread.service_account()
sh = gc.open(sheet_name)


def writeSite(url):
    site = urllib.request.urlopen("https://data.alexa.com/data?cli=10&url=http://" + url).read()
    tree = ET.parse(site)
    xml = tree.getroot()
    if(len(list(xml)) > 0):
        if(len(list(xml[0])) < 4):
            sh.sheet1.append_row([url, xml[0][0].attrib.get('TEXT')])
        else:
            sh.sheet1.append_row([url, xml[0][0].attrib.get(
                'TEXT'), xml[0][3].attrib.get('CODE'), xml[0][3].attrib.get('RANK')])
    time.sleep(3)

def writeCategory(url):
    client = Client('at_2P50aD7BIrirqswZhTcgUC8CFrXbi')
    response = client.data('whoisxmlapi.com')
    print(response)
    count = 0
    if response.website_responded:
        for cat in response.categories:
            if cat.tier1:
                if(str(cat.tier1.name) != "Not enough content" and count < 1):
                    sh.sheet1.append_row([url, str(cat.tier1.name)])
                    count += 1
    else:
        sh.sheet1.append_row([url, "No Data"])

    time.sleep(3)

def readCsv(file, site):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if(site):
                print(row[1])
            else:
                print(row[0])
            if(site):
                writeSite(row[1])
            else:
                writeCategory(row[0])

readCsv('sitesused.csv', False)
