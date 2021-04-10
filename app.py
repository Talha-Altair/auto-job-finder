import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from newspaper import Article
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import time

cluster = MongoClient('mongodb+srv://<username>:<password>@cluster0.xvmvm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority') #Enter your Mongo Cluster Connection Code here
db = cluster["JR"]  #Enter your database name 
collection = db["TS"]   #Enter your collection name
PATH ="/home/talha/Downloads/chromedriver_linux64/chromedriver" #Driver Path location
driver = webdriver.Chrome(PATH)

def collect_data(driver,i):
    lnks=driver.find_elements_by_class_name("title")
    for lnk in lnks:
        i+=1
        lnk=(lnk.find_element_by_css_selector('a').get_attribute('href'))
        url = lnk
        print(lnk)
        article = Article(url)
        article.download()
        article.parse()
        collection.insert_one({"link": lnk, "Data": article.text })

driver.get("https://in.indeed.com")


search = driver.find_element_by_id("text-input-what")
search.send_keys("Data Scientist")
search.send_keys(Keys.RETURN)


collect_data(driver,0)

def func(i):
    print("talha" + i)

for j in range(4): #Number of pages to scrap
    driver.get("https://in.indeed.com/jobs?q=data+scientist&start=" + str((j+1)*10))
    collect_data(driver,j)
