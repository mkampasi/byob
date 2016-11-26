#!/usr/bin/python

from flask import Flask,request, send_from_directory, url_for, jsonify
import urllib2
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.25/bin/chromedriver') 

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/login', methods=['POST'])
def login():
    skillset=[] #Users skills will be stored in this list
    #Fetch POST parameters
    userid=request.form['userid']
    profile_link=request.form['url'].encode('utf-8')
    #Get all user's skills from Linkedin
    driver.get(profile_link)
    html=driver.page_source
    soup=BeautifulSoup(html) #specify parser or it will auto-select for you
    skill_list=soup.find('ul', class_='pills')
    #remove "See less / See more"
    for row in skill_list.findAll("li"):
        if("see" in row.text.lower()):
            continue
        skillset.append(row.text.lower())
    driver.quit()
    #Connect to DB 
    client = MongoClient()
    db = client.byob
    coll = db.users
    #Update/insert skills in DB
    key = {'userid':userid}
    data = {'$set':{'userid':userid,'skills':skillset}}
    coll.update(key, data,upsert=True)
    return "success"

if __name__ == '__main__':
    app.run()
