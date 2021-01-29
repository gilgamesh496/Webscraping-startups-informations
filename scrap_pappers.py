import csv
import requests
from bs4 import BeautifulSoup 
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs 
from time import sleep
import pandas as pd
from functools import reduce
import re

path='/usr/local/bin/chromedriver2'    
driver = webdriver.Chrome(path)

siret = pd.read_csv("/Users/thomasclement/Documents/M2 TSE/Contrat pro/BDD/code_post.csv", sep=";")
startups = siret[siret != ""]
startups = startups['siret'].to_list()
url = 'https://www.pappers.fr/'

code_post = []
création = []
for startup in startups:
    driver.get(url)
    sleep(1.5)
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/form/div/div[1]/input').send_keys(startup)
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/form/div/div[2]/button').click()
   
    try: 
        codepost = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div[1]/p[2]').text
        codepost = re.findall(r"\D(\d{5})\D", codepost)[0]
    except: 
        codepost = 'NA'
    
    code_post.append(codepost)
   
    try:
        date_creation = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div[4]/p[2]').text
    except: 
        date_creation = 'NA'
        
    création.append(date_creation)
    sleep(1.5)


codepost = pd.DataFrame(code_post,création).reset_index()

codepost.to_csv('codepost.csv', index=False)
