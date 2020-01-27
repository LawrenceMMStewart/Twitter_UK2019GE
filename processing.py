#old version:

import gzip
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dateutil.parser import parse

"""
with gzip.GzipFile("tweets.json", 'r') as fin:
    # data = json.loads(fin.read().decode('utf-8'))

    data=[json.loads(tweet.decode('utf-8')) for tweet in fin.readlines()]
    print(data[2])
    print("len of data is ",len(data))

"""

#my version:

def GetTweets(k):
	"""
	retrieves k tweets in json form, uncompressing them and adding to list
	"""

	with gzip.open('tweets.json', 'rb') as f:
	    file_content = []
	    for i in range(k):
	    	file_content.append(f.readline())
	return file_content


def GetAllTweets():
	"""
	retrieves all tweets in json form, uncompressing them and adding to list
	"""
	with gzip.open('tweets.json','rb') as f:
		file_content=[]
		for line in f:
			file_content.append(line)
	return file_content



def Bytes_to_Json(bytelist):
	"""
	converts a list of tweets in byte form (text) into json dicts
	"""
	return [json.loads(x.decode('utf-8')) for x in bytelist]



def date_range(tweet_list,start_date,end_date):
	"""
	filters a list of tweets, keeping only those that fall
	into a user defined range of dates given by the variables
	start and end

	e.g. start=datetime.datetime(2019, 12, 9, 17, 45, 29)
	"""
	def predicate(x):
		#parse x's date and remove utc information -- 
		dt=parse(x['created_at']).replace(tzinfo=None)
		return start_date<=dt <=end_date

	return list(filter(predicate,tweet_list))


def date_extract(tweet):
	"""
	Extracts the date of the tweet:
	"""
	dt=parse(tweet['created_at'])
	return dt.date()


def tweet_type(tweet):
	"""
	Classifies a tweet object into one of 4 categories:
	0 - std
	1 - extended
	2 - retweet
	3 - quoted 
	"""
	if "quoted_status" in tweet.keys():
		return 3
	elif "retweeted_status" in tweet.keys():
		return 2
	elif "extended_tweet" in tweet.keys():
		return 1 
	else:
		return 0 

def tweet_text(tweet,category):
	"""
	returns the user written text of a tweet given the tweets category:
	to find the category use the tweet_type function above.
	"""
	#plain tweet
	if category==0:
		return tweet['text']
	#extended tweet
	elif category==1:
		return tweet['extended_tweet']['full_text']
	#retweeted status
	elif category==2:
		sub_tw=tweet['retweeted_status']
		sub_lab=tweet_type(sub_tw)
		return tweet_text(sub_tw,sub_lab)
	#quoted status	
	else:
		sub_tw=tweet['quoted_status']
		sub_lab=tweet_type(sub_tw)
		return tweet_text(sub_tw,sub_lab)

#examples of some utils being used

if __name__=="__main__":

	#little example:
	#load sentiment analyzer
	sid = SentimentIntensityAnalyzer()


	#uncompress selected raw sample
	raw_sample=GetTweets(100)
	sample=Bytes_to_Json(raw_sample)
	print(sample[0])

	#classify type of tweets i.e. retweet, quoted tweet e.c.t
	tw_types=list(map(tweet_type,sample))

	#exctract texts and score sentiment
	texts=list(map(tweet_text,sample,tw_types))
	sentiments=list(map(sid.polarity_scores,texts))
	dates=list(map(lambda x: x['created_at'],sample))
	breakpoint()

	# for i in range(10):
	# 	print(texts[i+20])
	# 	print(sentiments[i+20])


	#scp processing.py violette:./project
