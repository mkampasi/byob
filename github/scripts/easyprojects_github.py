#Program to extract the master list of languages from Github
import urllib2
import json
from urllib2 import HTTPError
import time
import re
start_url = "https://github.com/MunGell/awesome-for-beginners" 
page = urllib2.urlopen(start_url)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page)
jsonfout = open("../output/github_easyprojects.json","w+")
links=[]

#Crawl easy projects
links_list=soup.find('div', class_='readme')
for row in links_list.findAll('li'):
    for link in row.findAll('a'):
        link=link.attrs['href']
        if link.find('labels') <> -1:
            link=link[0:link.find('labels')-1]
        if "github" in link and "puppet" not in link:
            links.append(link)

#Crawl from issues search page for relevant labels
labels=["easy","beginner","starter"] 
for label in labels:
    start_url2 = "https://github.com/search?q=label%3A" + label + "+is%3Aopen"
    page = urllib2.urlopen(start_url2)
    soup = BeautifulSoup(page)
    menu_list=soup.find('div', class_='issue-list')
    for row in menu_list.findAll('p',{ "class":"title" }):
        for link in row.findAll('a'):
            link=link.attrs['href']
            link="https://github.com" +link[0:link.find('issues')-1]
            links.append(link)

links = list(set(links)) ##de-duplicate

    
def resolve_redirects(url):
    try:
        return urllib2.urlopen(url)
    except HTTPError, e:
        if e.code == 429:
             time.sleep(5);
             return resolve_redirects(url)
        if e.code == 404:
             return resolve_redirects(url)
        raise

with open('../output/easy_linkstocrawl.json') as f:    
    links = json.load(f) 
#Extract data from all crawled pages
resdict={}
finalres=[]
for eachlink in links:
    print eachlink
    resdict={}
    resdict["source"]="github"
    resdict["skillevel"]="easy"
    resdict["repo_name"]=eachlink[eachlink.rfind("/")+1:]
    page = resolve_redirects(link)
    soup = BeautifulSoup(page)
    resdict["repo_description"]=soup.find(itemprop="about").get_text()
    resdict["repo_link"]=eachlink
    for elem1 in soup(text=re.compile(r"Star")):
        resdict["stargazers"]= elem1.parent.parent.find('a',class_="js-social-count").get_text()
    
    lang_url = eachlink[0:eachlink.rfind("/")]
    lang_repo_name=eachlink[eachlink.rfind("/")+1:]
    page = resolve_redirects(lang_url)
    soup = BeautifulSoup(page)
    for elem in soup(text=re.compile(lang_repo_name)):
        elem = elem.parent
    while 1==1:
        if elem.find(itemprop="programmingLanguage") is not None:
            resdict["repo_language"] = elem.find(itemprop="programmingLanguage").get_text()
            break
        elif elem.findAll('span',{"class":"repo-language-color"}):
            if elem.findAll('p',{"class":"f6"}):
                resdict["repo_language"]=elem.findAll('p',{"class":"f6"})[0].get_text('|').split('|')[1]
            elif elem.findAll('span',{"class":"f6"}):
                resdict["repo_language"] = elem.findAll('span',{"class":"f6"})[0].text
            break
        elem=elem.parent
    finalres.append(resdict)
    
final_dump = json.dumps(finalres, indent=4)
jsonfout.write(final_dump)