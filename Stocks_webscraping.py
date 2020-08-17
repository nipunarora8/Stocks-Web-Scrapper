#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#files to install

# !pip install bs4
# !pip install selenium
# !pip install html5lib
# !pip install 


# In[ ]:


from selenium import webdriver
import pandas as pd
from datetime import date
import numpy as np
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()
# driver = webdriver.Chrome()

driver.get("https://www.screener.in/login/")


# In[ ]:


username = driver.find_element_by_id("id_username")
password = driver.find_element_by_id("id_password")
username.send_keys("****your-sceener-email-id********")
password.send_keys("*******your-screener-password*******")
driver.find_element_by_class_name("button-primary").click()


# In[ ]:


driver.refresh()
path = "https://www.screener.in/company/"


# In[ ]:


file=open("stocks.txt",'r')
data=file.read().split('\n')[:-1]
dict_df={}
for i in data:
    new_path = path+i+'/consolidated/'
    
    driver.get(new_path)
    time.sleep(2) #delay to let page open, increase for slower internet

    r_new=driver.page_source.encode('utf-8')

    soup = BeautifulSoup(r_new, 'html5lib')

    table1=soup.find_all('li', attrs={'class':'four columns'})

    list=[]
    for n in range(len(table1)):
        list.append(table1[n].text.replace('\n',"").replace(" ",""))

    list.remove('CompanyWebsite')
    list.remove('ListedonBSEandNSE')

    ratio=[]
    value=[]
    for j in list:
        if j[:11]=='52weeksHigh':
            continue
        ratio.append(j.split(':')[0])
        value.append(j.split(':')[1])
    ratio= np.array(ratio)
    value=np.array(value)

    dict_df[i]=value
    

df=pd.DataFrame(dict_df.values(),columns=ratio,index=dict_df.keys())
if "excel" not in os.listdir():
    os.mkdir("excel")
    df.to_csv("excel/"+str(date.today())+".csv")
else:
    df.to_csv("excel/"+str(date.today())+".csv")
driver.quit()
print("File created with name: {}.csv".format(str(date.today())))

