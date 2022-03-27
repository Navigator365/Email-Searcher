import csv
import gspread
import time
import urllib.request
import xml.etree.ElementTree as ET

# For official use, use Full Site Ranking
sheet_name = "bigtest"

gc = gspread.service_account()
sh = gc.open(sheet_name)


def writeSite(url):
    site = urllib.request.urlopen("https://data.alexa.com/data?cli=10&url=http://" + url)
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
    site = urllib.request.urlopen("https://website-categorization.whoisxmlapi.com/api/v2?apiKey=at_2P50aD7BIrirqswZhTcgUC8CFrXbi&domainName=" + url)
    tree = ET.parse(site)
    xml = tree.getroot()
    if(xml[2] is 1):
        sh.sheet1.append_row(url, xml[0][0].attrib.get('name'))
    else:
        sh.sheet1.append_row(url, "false")
    time.sleep(3)

def readCsv(file, site):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row[1])
            if(site):
                writeSite(row[1])
            else:
                writeCategory(row[0])



readCsv('sitesused.csv', False)
