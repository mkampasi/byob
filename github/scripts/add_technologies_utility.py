import json
import sys
from bs4 import BeautifulSoup
import urllib2
import re
reload(sys)  
sys.setdefaultencoding('utf8')
#Load master list of teachnologies 
with open('../output/'  + 'technologies.json') as tech_file:
    technologies = json.load(tech_file)

#Load master list of teachnologies 
with open('../output/'  + 'languages.json') as lang_file:
    languages = json.load(lang_file)
    
#Open the github crawled data
with open('../output/'  + 'github_easyprojects.json') as links_file:
    easyprojects = json.load(links_file)

others = [] 
     
#Perform unstructured extraction for technology names on the README.md file for each project
for record in easyprojects:
    url = record["repo_link"]
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    readme = soup.find('div', class_='readme')
    mergedlist = languages + technologies
    text = soup.findAll(text=True)
    text=list(text)
    text = [str(i.encode('utf-8').lower()) for i in text]
    text = map(str.strip, text)
    text = list(filter(None, text))
    
    others = [e for e in mergedlist if " " + e + " " in '\n'.join(text)]
    others=list(set(others))
    if others is not None:
        record["others"]=others
    else:
        record["others"]=""
    
f = open('../output/'  + 'github_easyproject2.json','w+')
f.write(json.dumps(easyprojects,indent=4))