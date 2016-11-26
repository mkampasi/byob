#!/usr/bin/python

from flask import Flask,request, send_from_directory, url_for, jsonify
import urllib2
import json
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.25/bin/chromedriver') #I actually used the chromedriver and did not test firefox, but it should work.



app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


#@app.route('/scrape', methods=['GET', 'POST'])
@app.route('/scrape')
def scrape():
    skillset=[]
    #profile_link=request.args.get('url')
    profile_link="https://www.linkedin.com/in/manishakampasi"
    driver.get(profile_link)
    html=driver.page_source
    soup=BeautifulSoup(html) #specify parser or it will auto-select for you
    skill_list=soup.find('ul', class_='pills')
    for row in skill_list.findAll("li"):
        if("see" in row.text.lower()):
            continue
        skillset.append(row.text.lower())
    driver.quit()
    return jsonify(skills=skillset)

if __name__ == '__main__':
    app.run()
