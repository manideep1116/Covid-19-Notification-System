from bs4 import BeautifulSoup
import requests
from urllib import request
import json
from urllib.request import urlopen
from selenium import webdriver
import os
import time



#url="https://data-stlcogis.opendata.arcgis.com/app/st-louis-county-covid-19-statistics"
url = "https://nytimes.com/interactive/2020/us/missouri-coronavirus-cases.html"
driver = webdriver.Chrome(executable_path='/Users/manideep/practice/Git_hub/Covid-19-Tracker/scrapping/chromedriver')
driver.get(url)
time.sleep(5)

page_html = driver.page_source
soup = BeautifulSoup(page_html, 'html.parser')

print(soup.prettify())
#c = soup.find_all("g", {'class' : 'responsive-text-label'})


#print(c)
# result = requests.get(url)
# soup = BeautifulSoup(result.content)
# print(soup)

#soup = BeautifulSoup(html_content, "lxml")
#soup = BeautifulSoup(html_content, 'html.parser')
#soup = BeautifulSoup(result.text, 'html.parser')
#print(soup.prettify()) # print the parsed data of html
# soup.find("div", class_ = "dock-element ember-view")
#print(tags = soup('text')

# #html = request.urlopen(url).read()
# soup = BeautifulSoup(html_content,'html.parser')
# site_json=json.loads(soup)

# print(site_json)
def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)
