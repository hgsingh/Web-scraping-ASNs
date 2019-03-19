#!/usr/bin/env python

#
# Web scraping
# ASNs (Autonomous System Numbers) are one of the building blocks of the
# Internet. This project is to create a mapping from each ASN in use to the
# company that owns it. For example, ASN 36375 is used by the University of
# Michigan - http://bgp.he.net/AS36375
# 
# The site http://bgp.he.net/ has lots of useful information about ASNs. 
# Starting at http://bgp.he.net/report/world crawl and scrape the linked country
# reports to make a structure mapping each ASN to info about that ASN.
# Sample structure:
#   {3320: {'Country': 'DE',
#     'Name': 'Deutsche Telekom AG',
#     'Routes v4': 13547,
#     'Routes v6': 268},
#    36375: {'Country': 'US',
#     'Name': 'University of Michigan',
#     'Routes v4': 14,
#     'Routes v6': 1}}
#
# When done, output the collected data to a json file.
#
# Use any python libraries. One suggestion, a good one for scraping is
# BeautifulSoup:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# 

import urllib2
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4
import json 
import re
# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
BASE_URL = "http://bgp.he.net"
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html)
    return soup
#Takes a country an returns a JSON object for its ASN
def getAsnsForCountry(country):
    countryJson = {}
    countryName = ""
    asnSize = 0
    #for i in range(len(countryData)):
    if(country.find('td').find('div', {'class':'down2 floatleft'})):
        countryName = country.find('td').find('div', {'class':'down2 floatleft'}).text.strip()
    if(country.find('td', {'class':'alignright'})):
        num = (re.findall('^[0-9]{1,3},[0-9]{3}|^[0-9]+$', country.find('td', {'class':'alignright'}).text.strip())[0])
        asnSize = int(num.replace(',', ''))
    #generate JSON here
    countryJson[countryName] = []
    center_aligned_cells = (country.findAll('td', {'class':'centeralign'}))
    for i in range(len(center_aligned_cells)):
        if(center_aligned_cells[i].find('a', href=True)):
            parseAsnFromSoup(url_to_soup(BASE_URL + center_aligned_cells[i].find('a', href=True)['href']))

    print countryName
    print asnSize
    
            
def parseAsnFromSoup(asnSoup):
    asnList = asnSoup.find('div', id='country').find('tbody').findAll('tr')
    asnJson = {}
    for i in range(len(asnList)):
        asnNumber = -1
        if(asnList[i].find('a', href=True)):
            asnNumber = asnList[i].find('a', href=True).text.strip()
            asnJson[asnNumber] = {}
        if(asnList[i].find('td')):
            asnJson[asnNumber]['Name'] = asnList[i].find('td').text.strip()
        if(asnList[i].findAll('td', {'class':'alignright'})):
            routeV4String = re.findall('^[0-9]{1,3},[0-9]{3}|^[0-9]+$', asnList[i].findAll('td', {'class':'alignright'})[1].text.strip())[0]
            routeV6String = re.findall('^[0-9]{1,3},[0-9]{3}|^[0-9]+$', asnList[i].findAll('td', {'class':'alignright'})[3].text.strip())[0]
            asnJson[asnNumber]['Routes v4'] = int(routeV4String.replace(',',''))
            asnJson[asnNumber]['Routes v6'] = int(routeV6String.replace(',',''))
        print asnJson
if __name__ == "__main__":
    soup = url_to_soup('http://bgp.he.net/report/world')
    country_soup = soup.find('div', id='countries').find('tbody').findAll('tr')
    for i in range(len(country_soup)):
        getAsnsForCountry(country_soup[i])
        

    