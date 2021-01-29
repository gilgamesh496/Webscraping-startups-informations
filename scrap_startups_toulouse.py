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

path='/usr/local/bin/chromedriver'    
driver = webdriver.Chrome(path)

company_url = []
url = 'https://www.annuaire-startups.pro/annuaire-startup/annuaire-startup-du-monde/annuaire-startup-europe/annuaire-startup-france/annuaire-startup-occitanie/annuaire-startup-haute-garonne/annuaire-startup-toulouse/page/'
url_list = []

#create the url list to scrap
for i in range(21) :
   if i > 0 :
       url1 = url + str(i) + '/'
       url_list.append(str(url1))
   
#def function to scrap the company information page

for url in url_list :
    r = requests.get(url)

    soup = BeautifulSoup(r.content)

    for link in soup.find_all('a', href=True):
        if "https://www.annuaire-startups.pro/startup/" in link.get("href"):
            company_url.append(str(link.get('href')))

#remove pairwise duplicates
for i in range(600) :
    company_url[0+i*2] = ""
comp_url = []
for string in company_url:
    if (string != ""):
        comp_url.append(string)       
             
#create dataframe for store all the data about each company
column_names = ["name", "ceo", "desc", "sect", "fund"]
scrap_su = pd.DataFrame(columns = column_names)
comp_ceo = []
comp_name = []
comp_desc = []
comp_fund = []
comp_sect = []

for url in comp_url :
    r = requests.get(url)

    soup = BeautifulSoup(r.content)
    try:
        name = soup.find("h1", {"class": "product_title entry-title"}).get_text()
    except:
        name = "NA"

    try:
        fund = soup.find("span", {"class": "woocommerce-Price-amount amount"}).get_text()
    except:
        fund = "NA"

    try:
        desc = soup.find("p", {"style": "text-align: justify;"}).get_text()              
    except:
        desc = "NA"
    try:
        sect = soup.find("div", {"class": "border-grey-bottom mt15 pb15 font90"}).get_text()  
    except:
        sect = "NA"
    try:
        ceo  = soup.find("div", {"class": "border-grey-bottom mt15 pb15 font90"}).get_text()
    except:
        ceo = "NA"
        
    comp_name.append(name)
    comp_fund.append(fund)
    comp_desc.append(desc)
    comp_sect.append(sect)
    comp_ceo.append(ceo)

df_name = pd.DataFrame(comp_name)
df_fund = pd.DataFrame(comp_fund)
df_desc = pd.DataFrame(comp_desc)
df_sect = pd.DataFrame(comp_sect)
df_ceo = pd.DataFrame(comp_ceo)     
       
frames = [df_name,ceo,df_desc,df_sect,df_fund]
su_scrap = pd.concat(frames, join='outer', axis=1)
su_scrap.columns = column_names

###trouver le secteur dans la description
sect2 = []
for row in comp_sect:
    row = row.split(".")[1]

ceo2 = []
for row in comp_ceo:
    ceo2.append(row.split(".")[0])
    

for row in comp_ceo:
    i = row.split(".")[0]
    i = i + "."
    e = re.search(r'par (.+?) en', i)
    if e:
        r = e.group(1)
        ceo2.append(str(r))
    else:
        e = re.search(r'par (.+?) .', i)
        if e:
            r = e.group(1)
            ceo2.append(str(r))
        else:
            ceo2.append('NA')

ceo = pd.DataFrame(ceo2)     

su_scrap.to_excel("/Users/thomasclement/Documents/M2 TSE/Contrat pro/BDD/su_scrap.xlsx")
