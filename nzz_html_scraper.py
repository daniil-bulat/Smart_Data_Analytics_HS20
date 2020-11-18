#@author: danielbulat

### ### ### NZZ Webscraper ### ### ###

# The Code for nzz web scraper explained
#
# First, we create four empty vectors, “date”, “title”, “teaser” and “date_link” 
# to which the extracted information is appended to later. Second, 
# a for loop generates URLs and the Chrome Webdriver opens the URL. 
# Third, using Chrome Webdriver and Selenium we select the html tags t
# hat contain the information we need in some of the first article containers 
# (these are the "blocks" of articles shown on the site), save the information 
# as text, and append it to the corresponding vector defined in the first step.
# 
# Our custom function “check_exists_by_class” checks if the 
# element we want to extract exists; if it does, it returns 
# its value in text format, otherwise it returns a “false” statement 
# and continues the loop. This step is important, as not all headlines 
# have a teaser and sometimes the headline is stored under a “teaser” tag. 
# Using “check_exists_by_class” the loop will not interrupt if the 
# information sought does not exist, which in itself is not an issue 
# because we know that, given the structure of nzz.ch, NA returns can occur. 
# 
# Then, we add a second date vector “date_link”. 
# This was necessary because older versions of nzz.ch, starting around 2014, 
# do not have the date the article was written stored in their meta data. 
# In these cases we simply use the date that version of nzz.ch was captured. 
# 
# Lastly, once the loop is complete, all vectors are merged to a data frame 
# and exported as a csv file, which is then imported into R, where the necessary 
# formatting changes are made before starting the sentiment analysis.
#
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import pandas as pd

# Directory
os.chdir('/Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/git_hub/qta2020/nzz_2013_2020')

# Install WebDriver
driver = webdriver.Chrome('/Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/chromedriver')


# Functions
def check_exists_by_class(driver, xpath):
    try:
        driver.find_element_by_class_name(xpath)
    except NoSuchElementException:
        return False
    return driver.find_element_by_class_name(xpath).text


htmls = pd.DataFrame(os.listdir(), columns = ['name'])
htmls = htmls.sort_values(by='name', ascending=0)
htmls.index = range(0,4884)


# Loop to extract date, title and teaser text from every element of "all_articles"
date = []
title = []
teaser = []


for i in range(0,len(htmls)):
    j = htmls.iloc[i,0]
    # URL where the document (folder) is saved !LOCALY!
    url = ('file:///Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/git_hub/qta2020/nzz_2013_2020/' + j + '')
    
    # Will open browser and go to the address defined in "url"
    driver.get(url)
    
    # Wait for the website to load
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='id-ld_1553418']/div[2]/a/h2/span")))
    time.sleep(3) # manual alternative to webdriverwait
    
    ########################################################################################################################################
    ########################################################################################################################################
    # Find all relevant articles in "url"
    all_articles = driver.find_elements_by_xpath("//*[@data-nzz-tid='container-exclusive']")
    
    for i in range(0,len(all_articles)):
        date.append(all_articles[i].find_element_by_class_name("metainfo__item.metainfo__item--date").text)
        title.append(all_articles[i].find_element_by_class_name("teaser__title-name").text)
        sub_step = check_exists_by_class(all_articles[i], "teaser__lead.teaser__lead--2of3.teaser__lead--regular")
        teaser.append(sub_step)
        
    time.sleep(3)
        
        

# Build data frame from looped extractions
date = np.array(date)
title = np.array(title)
teaser = np.array(teaser)
df = pd.DataFrame({'Date':date, 'Title':title, 'Teaser':teaser})

df_1 = df

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
# DF2
last_index = htmls.iloc[:,0][htmls.iloc[:,0]=='20200413114132.html'].index.tolist()
last_index = int("".join(map(str, last_index)))

htmls_2 = htmls.iloc[last_index:,0]


# Loop to extract date, title and teaser text from every element of "all_articles"
date = []
title = []
teaser = []


for i in range(78,len(htmls_2)):
    j = htmls_2.iloc[i]
    # URL where the document (folder) is saved !LOCALY!
    url = ('file:///Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/git_hub/qta2020/nzz_2013_2020/' + j + '')
    
    # Will open browser and go to the address defined in "url"
    driver.get(url)
    
    # Wait for the website to load
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='id-ld_1553418']/div[2]/a/h2/span")))
    time.sleep(3) # manual alternative to webdriverwait
    
    ########################################################################################################################################
    ########################################################################################################################################
    # Find all relevant articles in "url"
    all_articles = driver.find_elements_by_xpath("//*[@data-nzz-tid='container-exclusive']")
    
    for i in range(0,len(all_articles)):
        date.append(all_articles[i].find_element_by_class_name("metainfo__item.metainfo__item--date").text)
        title.append(all_articles[i].find_element_by_class_name("teaser__title-name").text)
        sub_step = check_exists_by_class(all_articles[i], "teaser__lead.teaser__lead--2of3.teaser__lead--regular")
        teaser.append(sub_step)
        
    time.sleep(3)
        
        

# Build data frame from looped extractions
date = np.array(date)
title = np.array(title)
teaser = np.array(teaser)
df = pd.DataFrame({'Date':date, 'Title':title, 'Teaser':teaser})

df_2 = df


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
# DF3
last_index = htmls.iloc[:,0][htmls.iloc[:,0]=='20200316050042.html'].index.tolist()
last_index = int("".join(map(str, last_index)))

htmls_3 = htmls.iloc[last_index:,0]


# Loop to extract date, title and teaser text from every element of "all_articles"
date = []
title = []
teaser = []


for i in range(last_index,len(htmls_3)):
    j = htmls_3.iloc[i]
    # URL where the document (folder) is saved !LOCALY!
    url = ('file:///Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/git_hub/qta2020/nzz_2013_2020/' + j + '')
    
    # Will open browser and go to the address defined in "url"
    driver.get(url)
    
    # Wait for the website to load
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='id-ld_1553418']/div[2]/a/h2/span")))
    time.sleep(3) # manual alternative to webdriverwait
    
    ########################################################################################################################################
    ########################################################################################################################################
    # Find all relevant articles in "url"
    all_articles = driver.find_elements_by_xpath("//*[@data-nzz-tid='container-exclusive']")
    time.sleep(2)
    
    for i in range(0,len(all_articles)):
        date.append(all_articles[i].find_element_by_class_name("metainfo__item.metainfo__item--date").text)
        title.append(all_articles[i].find_element_by_class_name("teaser__title-name").text)
        sub_step = check_exists_by_class(all_articles[i], "teaser__lead.teaser__lead--2of3.teaser__lead--regular")
        teaser.append(sub_step)
        
    time.sleep(3)
        
        

# Build data frame from looped extractions
date = np.array(date)
title = np.array(title)
teaser = np.array(teaser)
df = pd.DataFrame({'Date':date, 'Title':title, 'Teaser':teaser})

df_3 = df

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
# DF4
last_index = htmls.iloc[:,0][htmls.iloc[:,0]=='20191105024420.html'].index.tolist()
last_index = int("".join(map(str, last_index)))

htmls_4 = htmls.iloc[last_index:,0]


# Loop to extract date, title and teaser text from every element of "all_articles"
date = []
title = []
teaser = []


for i in range(last_index,len(htmls_4)):
    j = htmls_4.iloc[i]
    # URL where the document (folder) is saved !LOCALY!
    url = ('file:///Users/danielbulat/Desktop/Uni/UniSG/FS20/qta/GroupProject/git_hub/qta2020/nzz_2013_2020/' + j + '')
    
    # Will open browser and go to the address defined in "url"
    driver.get(url)
    
    # Wait for the website to load
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='id-ld_1553418']/div[2]/a/h2/span")))
    time.sleep(3) # manual alternative to webdriverwait
    
    ########################################################################################################################################
    ########################################################################################################################################
    # Find all relevant articles in "url"
    all_articles = driver.find_elements_by_xpath("//*[@data-nzz-tid='container-exclusive']")
    time.sleep(2)
    
    for i in range(0,len(all_articles)):
        date.append(all_articles[i].find_element_by_class_name("metainfo__item.metainfo__item--date").text)
        title.append(all_articles[i].find_element_by_class_name("teaser__title-name").text)
        sub_step = check_exists_by_class(all_articles[i], "teaser__lead.teaser__lead--2of3.teaser__lead--regular")
        teaser.append(sub_step)
        
    time.sleep(3)
        
        

# Build data frame from looped extractions
date = np.array(date)
title = np.array(title)
teaser = np.array(teaser)
df = pd.DataFrame({'Date':date, 'Title':title, 'Teaser':teaser})

df_4 = df



#####################################################################################################################################################################
#####################################################################################################################################################################
#####################################################################################################################################################################
# 20181227134329.html



# Quit browser, once this command is executed the browser will close
driver.quit()

frames = [df_1, df_2, df_3, df_4]

final_frame = pd.concat(frames)
final_frame.to_csv('nzz_2020_2019.csv', index=False, encoding='utf-8')















