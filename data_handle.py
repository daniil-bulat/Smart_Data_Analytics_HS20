#=============================================================================
#=============================================================================
#                              Reddit Reader
#                          Smart Data Analytics
#                         Universität St. Gallen
#
#                        Daniil Bulat 14-607-055
#                         Luca Riboni 14-619-878
#
#=============================================================================
#=============================================================================


#============================= Import Packages ===============================
import re
import pandas as pd
import numpy as np
import yfinance as yf
import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
% matplotlib inline

os.chdir("/Users/danielbulat/Desktop/Uni/HS20/SmartDataAnalytics/Smart_Data_Analytics_HS20/data")
 
#=============================== Functions ===================================
def IsNotNull(value):
	    return value is not None and len(value) > 0

 
def negated(word):

    if word.lower() in negate:
        return True
    else:
        return False
 
 
def polarity_check(dict, article):
  
    pos_count = 0
    neg_count = 0
 
    pos_words = []
    neg_words = []
 
    input_words = re.findall(r'\b([a-zA-Z]+n\'t|[a-zA-Z]+\'s|[a-zA-Z]+)\b', article.lower())
 
    word_count = len(input_words)
 
    for i in range(0, word_count):
        if input_words[i] in dict['Negative']:
            neg_count += 1
            neg_words.append(input_words[i])
        if input_words[i] in dict['Positive']:
            if i >= 3:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]) or negated(input_words[i - 3]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 2:
                if negated(input_words[i - 1]) or negated(input_words[i - 2]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 1:
                if negated(input_words[i - 1]):
                    neg_count += 1
                    neg_words.append(input_words[i] + ' (with negation)')
                else:
                    pos_count += 1
                    pos_words.append(input_words[i])
            elif i == 0:
                pos_count += 1
                pos_words.append(input_words[i])
 
    print('The # of positive words:', pos_count)
    print('The # of negative words:', neg_count)
    print('The list of found positive words:', pos_words)
    print('The list of found negative words:', neg_words)
    polarity_score = (pos_count - neg_count) /(pos_count + neg_count)
    print(polarity_score)
    results = [polarity_score]
    
    return results

def data_handle(data, currency, df_currency):
    df_currency = pd.read_csv(data)
    df_currency['Full text'] = df_currency["Title"]+ ". " + df_currency["Text"].map(str)
    df_currency = np.array(df_currency)

    scores = []
    for i in df_currency[:,7]:
        try:
            scores.append(polarity_check(dictionary,i))

        except:
            scores.append("0")
            pass
    df_currency = pd.DataFrame(df_currency)
    df_currency.columns =['Post ID', 'Title',"Text", "Score", "Publish Date", "al No. of Comments", "url", "Full Text" ] 
    df_currency["Polarity score"] = pd.DataFrame(scores)
    df_currency["Polarity score"] = df_currency["Polarity score"].astype(float)
    df_currency['Publish Date'] = df_currency['Publish Date'].astype('datetime64[ns]')



    dayly_mean_currency = df_currency.resample('d', on='Publish Date').mean().dropna(how='all')
    monthly_mean_currency = df_currency.resample('m', on='Publish Date').mean().dropna(how='all')
    weekly_mean_currency = pd.DataFrame(df_currency.groupby(df_currency["Publish Date"].dt.weekofyear)['Polarity score'].mean())
    print (dayly_mean_currency)
    print (monthly_mean_currency)
    print(weekly_mean_currency)
    results= df_currency, dayly_mean_currency, monthly_mean_currency, weekly_mean_currency
    return results





#================================= Dictionary ================================
## Positive Words Dictionary
dict_p = []
f = open('lmhdictp.txt', 'r')
for line in f:
	t = line.strip().lower()
	if IsNotNull(t):
		dict_p.append(t)
f.close

## Negative Words Dictionary
dict_n = []
f = open('lmhdictn.txt', 'r')
for line in f:
	t = line.strip().lower()
	if IsNotNull(t):
		dict_n.append(t)
f.close

## Complete Dictionary
dictionary = {'Negative': dict_n,
         'Positive': dict_p}

negate = []
f = open('negate.txt', 'r')
for line in f:
	t = line.strip().lower()
	if IsNotNull(t):
		negate.append(t)





#============================ Sentiment Analysis =============================
df_BTC, daily_mean_BTC, monthly_mean_BTC, weekly_mean_BTC = data_handle("reddit_bitcoin.csv", "BTC", "df_BTC")
df_ETH, daily_mean_ETH, monthly_mean_ETH, weekly_mean_ETH = data_handle("reddit_eth.csv", "ETH", "df_ETH")

btc = yf.download("BTC-USD", start="2015-01-02", end="2020-12-02")
eth = yf.download("ETH-USD", start="2015-01-02", end="2020-12-02")

btc=btc.drop(['Open', 'High',"Low","Adj Close", "Volume"], axis=1)
eth=eth.drop(['Open', 'High',"Low","Adj Close", "Volume"], axis=1)

btc["Publish Date"]=btc.index
eth["Publish Date"]=eth.index
daily_mean_BTC['Publish Date'] = daily_mean_BTC.index
daily_mean_ETH['Publish Date'] = daily_mean_ETH.index

r = pd.date_range(start=daily_mean_BTC["Publish Date"].min(), end=daily_mean_BTC["Publish Date"].max())
daily_mean_ETH=daily_mean_ETH.set_index('Publish Date').reindex(r).fillna(0).rename_axis('Publish Date').reset_index()
eth=eth.set_index('Publish Date').reindex(r).fillna(0).rename_axis('Publish Date').reset_index()
daily_mean_BTC=daily_mean_BTC.set_index('Publish Date')
daily_mean_ETH=daily_mean_ETH.set_index('Publish Date')
btc=btc.set_index('Publish Date')
eth=eth.set_index('Publish Date')

daily_returns = pd.DataFrame([])
daily_returns["Publish Date"]= btc.index
daily_returns=daily_returns.set_index('Publish Date')
daily_returns["BTC polarity score"]=daily_mean_BTC["Polarity score"]
daily_returns["ETH polarity score"]=daily_mean_ETH["Polarity score"]
daily_returns["BTC"]=btc["Close"]
daily_returns["ETH"]=eth["Close"]



#============================== Word Clouds ===================================
## BTC
btc_text = " ".join(review for review in df_BTC["Full Text"])

# Create and generate a word cloud image:
btc_stopwords = set(STOPWORDS)
btc_stopwords.update(["New","will","way","use","one","nan","https"])

btc_wordcloud = WordCloud(collocations=False, stopwords=btc_stopwords, background_color="white").generate(btc_text)

plt.imshow(btc_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

## ETH
eth_text = " ".join(review for review in df_ETH["Full Text"])

# Create and generate a word cloud image:
eth_stopwords = set(STOPWORDS)
eth_stopwords.update(["use","game","Please","nan"])

eth_wordcloud = WordCloud(collocations=False, eth_stopwords=stopwords, background_color="white").generate(eth_text)

plt.imshow(eth_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



#================================= OLS =======================================
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std



















