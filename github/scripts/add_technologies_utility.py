import json
import sys
from bs4 import BeautifulSoup
import urllib2
import re
from requests.exceptions import HTTPError

reload(sys)  
sys.setdefaultencoding('utf8')
#Load master list of teachnologies 
with open('../output/'  + 'technologies.json') as tech_file:
    technologies = json.load(tech_file)

#Load master list of teachnologies 
with open('../output/'  + 'languages.json') as lang_file:
    languages = json.load(lang_file)
    
#Open the github crawled data
with open('../output/'  + 'showcase_v1.2_master_dump.json') as links_file:
    easyprojects = json.load(links_file)

others = [] 
     
#Perform unstructured extraction for technology names on the README.md file for each project
for record in easyprojects:
    url = record["repo_link"]
    print "Processing :: " + url
    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'Error occurred for link :: ' + url
        continue

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
    
f = open('../output/'  + 'github_final_dump.json','w+')
f.write(json.dumps(easyprojects,indent=4))