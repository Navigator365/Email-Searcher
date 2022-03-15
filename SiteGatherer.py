import csv
import gspread
import time
import urllib.request
import xml.etree.ElementTree as ET

gc = gspread.service_account()
sh = gc.open("Full Site Ranking")


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
    time.sleep(2)


def readCsv(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row[1])
            writeSite(row[1])


readCsv('sample.csv')
