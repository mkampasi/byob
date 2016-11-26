#Program to extract the master list of languages from Github
import urllib2
import json
wiki = "https://github.com/trending"
page = urllib2.urlopen(wiki)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page)
jsonfout = open("../output/languages.json","w+")
languages=[]
menu_list=soup.find('div', class_='one-fourth')
for row in menu_list.findAll("span"):
    languages.append(row.text.lower())
final_dump = json.dumps(languages, indent=4)
jsonfout.write(final_dump)