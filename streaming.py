import tweepy
#tester
import sys
from tweepy.streaming import StreamListener
from datetime import datetime
import time 
import signal
import sys
import json
import gzip
from urllib3.exceptions import ProtocolError


# pierres
auth = tweepy.OAuthHandler('key1','key2')
auth.set_access_token('key3', 'key4')

api = tweepy.API(auth)

"""
track

A comma-separated list of phrases which will be used to determine what 
Tweets will be delivered on the stream. A phrase may be one or more terms 
separated by spaces, and a phrase will match if all of the terms in the 
phrase are present in the Tweet, regardless of order and ignoring case. By 
this model, you can think of commas as logical ORs, while spaces are 
equivalent to logical ANDs (e.g. ‘the twitter’ is the AND twitter, 
and ‘the,twitter’ is the OR twitter).
"""

track_list=""
track_list+="Brexit"
track_list+=',Boris Johnson'
track_list+=',Jeremy Corbyn'
track_list+=',Jo Swinson'
track_list+=',Nigel Farage'
track_list+=",Conservative party"
track_list+=",Labour party"
track_list+=",Brexit party"
track_list+=",Liberal Democrats"
track_list+=",Lib dems"

#convert to list
track_list=[track_list]


class FileWriteListener(StreamListener):

    def __init__(self ):
        super(StreamListener, self).__init__()
        # self.save_file = open('tweets.json','a')
        self.save_file=gzip.GzipFile('tweets.json','a')
        self.tweets = ""
        self.counter=0
        self.n_tweets=100

    def on_data(self, tweet):

        # self.tweets.append(json.loads(tweet))
        # self.save_file.write(str(tweet))
       
        self.tweets=self.tweets+json.dumps(json.loads(tweet))+'\n'
        self.counter+=1
        #compress and write every n tweets
        if self.counter==self.n_tweets:
          self.save_file.write(self.tweets.encode('utf-8'))
          self.tweets=""
          self.counter=0
      #   with gzip.GzipFile(jsonfilename, 'w') as fout:
          # fout.write(json.dumps(data).encode('utf-8'))  

    def on_error(self, status):
        print(status)
        return True



listener=FileWriteListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

while True:

	try:
	    print('Start streaming.')
	    f=open("stream_timings.txt","a")
	    f.write("\n")
	    f.write("streaming was initiated at"+" "+str(datetime.now())+"\n")
	    f.close()
	    stream.filter(languages=['en'],track=track_list)
	#comment out in order to allow keyboard interrupt

	# except KeyboardInterrupt as e:
	#     print("Stopped.")

	except (ProtocolError, AttributeError):
		continue
	finally:
	    print('Stream terminated.')
	    stream.disconnect()
	    # output.close()
	    f=open("stream_timings.txt","a")
	    f.write("streaming was stopped at"+" "+str(datetime.now())+"\n")
	    f.close()


