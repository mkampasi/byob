from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.25/bin/chromedriver') #I actually used the chromedriver and did not test firefox, but it should work.
profile_link="http://www.linkedin.com/in/manishakampasi"
driver.get(profile_link)
html=driver.page_source
soup=BeautifulSoup(html) #specify parser or it will auto-select for you
skill_list=soup.find('ul', class_='pills')
for row in skill_list.findAll("li"):
    print row.text.lower()
driver.quit()