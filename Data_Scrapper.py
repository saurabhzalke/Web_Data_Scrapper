#!/usr/bin/env python
# coding: utf-8

# In[101]:


# Below is a program which implements data
# scrapping using BeautifulSoup which is 
# a Python library for data scrapping.

# Loading necessary modules 
import requests
from bs4 import BeautifulSoup

r=requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c= r.content
soup =BeautifulSoup(c,"html.parser")

all = soup.find_all("div", {"class":"propertyRow"})
all[0].find("h4", {"class":"propPrice"}).text.replace("\n", "").replace(" ", "")

page_nr =soup.find_all("a", {"class":"Page"})[-1].text
# print(page_nr)

# Using a list to store the scrapped data.
l=[]

# If site has multiple pages, the program iterates through 
base_url="http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=" #URL of site to be scrapped

for page in range(0, int(page_nr)*10, 10):
    r= requests.get(base_url+str(page)+".html",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c= r.content
    soup= BeautifulSoup(c, "html.parser")
    all =soup.find_all("div",{"class":"propertyRow"})
    
    for item in all:
        d={}
        
        d["Address"] = item.find_all("span",{"class", "propAddressCollapse"})[0].text
        d["Locality"] = item.find_all("span",{"class", "propAddressCollapse"})[1].text
        d["Price"] = item.find("h4", {"class":"propPrice"}).text.replace("\n", "").replace(" ", "")
        try:
            d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"]= None

        try:
            d["Area"] = item.find("span", {"class", "infoSqft"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Bath"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"] = None

        try:
            d["Half Bath"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"] = None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class":"featureGroup"}), column_group.find_all("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text    

        l.append(d)
    
#Converting data into a data frame.
import pandas
df = pandas.DataFrame(l)

#Outputting the data to file.
df.to_csv("Fetched_data.csv")


# In[ ]:




