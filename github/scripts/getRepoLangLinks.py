import requests
from bs4 import BeautifulSoup

link_prefix = "https://github.com/trending/"

r = requests.get(link_prefix.strip())
soup = BeautifulSoup(r.content,'html.parser')
repo_lang_tag = soup.find_all("a",{"class" : "select-menu-item"})

all_lang_links_file = open("../output/allLangLinks.txt","w+")
links=[]
for row in repo_lang_tag:
	if(row is not None):
		all_lang_links_file.write(row['href'].strip() + '\n')

print "Done!"