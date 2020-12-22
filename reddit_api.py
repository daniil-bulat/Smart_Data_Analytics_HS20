#=============================================================================
#=============================================================================
#                              Reddit Reader
#                          Smart Data Analytics
#                         Universität St. Gallen
#
#                              Daniil Bulat
#                                Luca Riboni
#
#=============================================================================
#=============================================================================
import requests
import json
import csv
import datetime
import numpy as np
#=================================  FUNCTIONS  ===============================
def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/'+str(endpoint)+'/?title='+str(query)+'&size='+str(size)+'&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def collectSubData(subm):
    # keys = ['title', 'url', 'id', 'score', ' created_utc', 'num_comments']
    # list_ = [subm[i] if i in subm.keys() else np.nan for i in keys]
    
    subData = list() #list to store data points
    title = subm['title']
    #text = subm['selftext']
    if "selftext" in subm.keys():
        
        text = subm['selftext']
    else:
       text = np.nan
    url = subm['url']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']

    subData.append((sub_id,title,text,score,created,numComms,url))
    subStats[sub_id] = subData


def updateSubs_file():
    upload_count = 0
    location = '/Users/danielbulat/Desktop/Uni/HS20/SmartDataAnalytics/Group Project/Reference_Project/Reddit_API/'
    filename = 'reddit_eth.csv'
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Text","Score","Publish Date","Total No. of Comments","url"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
        print(str(upload_count) + " submissions have been uploaded")

def collectCommentData(subm):
    subData = list() #list to store data points
    body = subm['body']
    ID = subm['id']
    link_id = subm['link_id']
    parent_id = subm['parent_id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0

    subData.append((body,ID,link_id,parent_id,score,created))
    subStats[link_id] = subData

def updateComment_file():
    upload_count = 0
    location = '/Users/danielbulat/Desktop/Uni/HS20/SmartDataAnalytics/Group Project/Reference_Project/Reddit_API/'
    filename = 'reddit_comment_test.csv'
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Comment","ID","Link ID","Parent ID","Score","Publish Date"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1

        print(str(upload_count) + " submissions have been uploaded")

#=================================    SCRAPING   =============================
endpoint = "submission" # comment; submission; subreddit
sub ='ethereum'
# for dates: https://www.unixtimestamp.com/index.php
before = "1606780800"
after = "1420070400"
query = "ethereum"
size = "10000"
subCount = 0
subStats = {}

data = getPushshiftData(query, after, before, sub)

#=================================  SUBMISSIONS  =============================

while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)

print(str(len(subStats)) + " submissions have been added to list")


updateSubs_file()


#=================================  COMMENTS  ================================

while len(data) > 0:
    for comment in data:
        collectCommentData(comment)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)


updateComment_file()



#=================================  Merge csv  ===============================
import os
import glob
import pandas as pd
os.chdir("/Users/danielbulat/Desktop/Uni/HS20/SmartDataAnalytics/Group Project/Reference_Project/Reddit_API/merge")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv = pd.concat([pd.read_csv("reddit_2015_2017.csv"), pd.read_csv("reddit_2017_2020.csv")])
#export to csv
combined_csv.to_csv( "reddit_bitcoin.csv", index=False, encoding='utf-8-sig')










