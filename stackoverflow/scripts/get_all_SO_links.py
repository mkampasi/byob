#Program to extract the master list of languages from Github
import urllib2
import json
start_url = "http://stackoverflow.com" 
page = urllib2.urlopen(start_url+"/tags")
from bs4 import BeautifulSoup
soup = BeautifulSoup(page)
jsonfout = open("../output/linkstocrawl.json","w+")
tags=[]
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="tags-browser") 
rows = table.findAll(lambda tag: tag.name=='td')
for row in rows:
    tags.append(start_url + row.contents[1].attrs['href'] + "?sort=frequent")
final_dump = json.dumps(tags, indent=4)
jsonfout.write(final_dump)