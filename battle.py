import json
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import re

airindia_path='./airline_tweets/AirIndia.txt' 
airasia_path= './airline_tweets/AirAsia.txt'
indigo_path=  './airline_tweets/Indigo.txt'
emirates_path='./airline_tweets/Emirates.txt'


t_ai = []
t_aa = []
t_in = []
t_em = []

Tweet_File = open(airindia_path,"r")
for line in Tweet_File:
	try:
		t_ai.append(json.loads(line)) 
	except:
		continue

Tweet_File = open(airasia_path,"r")
for line in Tweet_File:
	try:
		t_aa.append(json.loads(line)) 
	except:
		continue

Tweet_File = open(indigo_path,"r")
for line in Tweet_File:
	try:
		t_in.append(json.loads(line)) 
	except:
		continue

Tweet_File = open(emirates_path,"r")
for line in Tweet_File:
	try:
		t_em.append(json.loads(line)) 
	except:
		continue
# record the no of tweets
tweet_no_ai =  len(t_ai)
tweet_no_aa =  len(t_aa)
tweet_no_em =  len(t_em)
tweet_no_in =  len(t_in)

ai_df = pd.DataFrame()
aa_df = pd.DataFrame()
in_df = pd.DataFrame()
em_df = pd.DataFrame()

# generate a data frame for the tweets
ai_df['text'] = map(lambda t: t['text'],t_ai)
ai_df['lang'] = map(lambda t: t['lang'],t_ai)
ai_df['friends'] = map(lambda t: t['user']['friends_count'],t_ai)
ai_df['followers'] = map(lambda t: t['user']['followers_count'],t_ai)
ai_df['statuses'] = map(lambda t: t['user']['statuses_count'],t_ai)

aa_df['text'] = map(lambda t: t['text'],t_aa)
aa_df['lang'] = map(lambda t: t['lang'],t_aa)
aa_df['friends'] = map(lambda t: t['user']['friends_count'],t_aa)
aa_df['followers'] = map(lambda t: t['user']['followers_count'],t_aa)
aa_df['statuses'] = map(lambda t: t['user']['statuses_count'],t_aa)

in_df['text'] = map(lambda t: t['text'],t_in)
in_df['lang'] = map(lambda t: t['lang'],t_in)
in_df['friends'] = map(lambda t: t['user']['friends_count'],t_in)
in_df['followers'] = map(lambda t: t['user']['followers_count'],t_in)
in_df['statuses'] = map(lambda t: t['user']['statuses_count'],t_in)

em_df['text'] = map(lambda t: t['text'],t_in)
em_df['lang'] = map(lambda t: t['lang'],t_in)
em_df['friends'] = map(lambda t: t['user']['friends_count'],t_in)
em_df['followers'] = map(lambda t: t['user']['followers_count'],t_in)
em_df['statuses'] = map(lambda t: t['user']['statuses_count'],t_in)

# study the text and do a sentiment analysis


import nltk # Natural Language processing 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def TwitterFeels(DataFrame):
	tot = len(DataFrame)
	twts  = DataFrame['text']
	happy,sad,neutral = 0,0,0
	sid = SentimentIntensityAnalyzer()
	for t in twts:
		ss = sid.polarity_scores(t)
		sad = sad + ss['neg']
		neutral = neutral + ss['neu']
		happy = happy + ss['pos']
	return (happy/tot,sad/tot,neutral/tot)

h_ai,s_ai,n_ai = TwitterFeels(ai_df) # happy_index,sad_index,neutral_index
h_aa,s_aa,n_aa = TwitterFeels(aa_df)
h_in,s_in,n_in = TwitterFeels(in_df)
h_em,s_em,n_em = TwitterFeels(em_df)

# some fancy metrics to find popularity,satisfaction,delay 
p_ai = (n_ai*5 + h_ai*20 - s_ai*20)/0.25
p_aa = (n_aa*5 + h_aa*20 - s_aa*20)/0.25
p_in = (n_in*5 + h_in*20 - s_in*20)/0.25
p_em = (n_em*5 + h_em*20 - s_em*20)/0.25

popularity = [p_ai,p_aa,p_in,p_em]
airlines = ('Air-India','Air-Asia','Indigo','Emirates')
y_pos = np.arange(len(airlines))

plt.plot(y_pos,popularity)
plt.xticks(y_pos,airlines)
plt.ylabel('Popularity index')
plt.xlabel('Airlines')
plt.title('Popularity of Airlines')
plt.show()

# Happiness index
# while calculating also take into account the other datas of the user like status_count,followers,following


def imp(followers,friends,statuses):
	impo = 1	
	if(followers < 100 and statuses < 100): # common people 
		impo = 10
	elif(followers < 1000 and statuses < 1000):
		impo = 8
	elif(followers/(friends+1) > 20):
		impo = 5
	elif(statuses < 500):
		impo = 2
	return impo

def Likes(DataFrame):
	tot = len(DataFrame)
	twts  = DataFrame['text']
	happy,sad,neutral = 0,0,0
	fo,fr,st = DataFrame['followers'],DataFrame['friends'],DataFrame['statuses']
	sid = SentimentIntensityAnalyzer()
	ctr = 0	
	for t in twts:
		ss = sid.polarity_scores(t)
		sad = sad + ss['neg']*imp(fo[ctr],fr[ctr],st[ctr])
		happy = happy + ss['pos']*imp(fo[ctr],fr[ctr],st[ctr])
		ctr=ctr + 1 	
	return (happy-sad)

print Likes(ai_df)
print Likes(aa_df)
print Likes(in_df)
print Likes(em_df)


# Report Delay,Maintainence etc etc records

def search(word,text):
	for w in word:
		w = w.lower()
		text = text.lower()
		match = re.search(w,text)
		if match : 
			return True
	return False

delay = []
maint = [] 

sid = SentimentIntensityAnalyzer()

def delay_fun(DataFrame):
	count = 0
	for i in DataFrame['text']:
		if(search(['delay','late','time','miss'],i) and sid.polarity_scores(i)['neg'] > 0.3):
			count = count + 1 
	delay.append(count) 	

def mainten_fun(DataFrame):
	count = 0
	for i in DataFrame['text']:
		if(search(['dirty','clean','hygiene','health','food','safety','meal'],i) and sid.polarity_scores(i)['neg'] > 0.3):
			count = count + 1 
	maint.append(count) 

delay_fun(ai_df)
delay_fun(aa_df)
delay_fun(in_df)
delay_fun(em_df)

mainten_fun(ai_df)
mainten_fun(aa_df)
mainten_fun(in_df)
mainten_fun(em_df)

N = 4
delay = tuple(delay)
maint = tuple(maint)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       

p1 = plt.bar(ind, delay , width)
p2 = plt.bar(ind, maint , width)

plt.ylabel('Scores')
plt.title('Tweets related to maintenance and delay records')
plt.xticks(ind, ('AirIndia', 'AirAsia', 'Indigo', 'Emirates'))
plt.legend((p1[0], p2[0]), ('delay', 'maintenance'))

plt.show()



