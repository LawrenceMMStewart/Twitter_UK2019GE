import gzip
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dateutil.parser import parse
from processing import * 


###################################################
"""
Filter tweets by date. Adding the date to a hashtable
each time a new date is created and added, have its value
pointing to a hashtable of that date - containing:

1) # keywords i.e. # of tweets about boris e.c.t
2) mean sentimentality that day
3) mean sentimentality about each keyword i.e. boris
4) -- can add more: 
"""
###################################################


class TweetDayFrame():
    """
    Structure to hold sentiments of tweets via keys,
    storing the data by day. 

    """

    def __init__(self,NLP_kit=SentimentIntensityAnalyzer()):
        self.keywords=[]
        self.keywords.append("Brexit")
        self.keywords.append('Boris Johnson')
        self.keywords.append('Jeremey Corbyn')
        self.keywords.append('Jo Swinson')
        self.keywords.append('Nigel Farage')
        self.keywords.append('Conservative party')
        self.keywords.append('Labour party')
        self.keywords.append('Brexit party')
        self.keywords.append('Liberal Democrats')
        self.keywords.append("Lib dems")

        #number of each keywords
        self.nkeywords=["n "+key for key in self.keywords]
        #mean sentiment of each keyword
        self.mskeywords=["ms "+key for key in self.keywords]

        #creates the dates hash table
        self.dates={}    

        #sentiment analyser:
        self.sid=NLP_kit

    def new_date(self,date_obj):
        """
        adds a new date to the self.dates hash map
        """
        new_dict={}
        new_dict["no_tweets"]=0
        #overall sentiment
        new_dict["os"]=0
        
        for nkey in self.nkeywords:
            #number of tweets for each key 
            new_dict[nkey]=0
        for mskey in self.mskeywords:
            #mean sentiment of key
            new_dict[mskey]=0
        
        self.dates[date_obj]=new_dict



    def update_stats(self,date_obj,key,tw_sent):
        """
        update the current stats of a date, given a key
        e.g. date_obj= datetime and key = "Brexit"
        """

        #first update the number of tweets on this day
        nprev=self.dates[date_obj]["no_tweets"]
        self.dates[date_obj]["no_tweets"]=nprev+1

        #update overall mean sentiment
        sprev=self.dates[date_obj]["os"]
        self.dates[date_obj]["os"]=((sprev*nprev)+tw_sent)/(nprev+1)

        #update nkey mskey, the number and mean sentiment of key
        nkprev=self.dates[date_obj]["n "+key]
        mskprev=self.dates[date_obj]["ms "+key]

        self.dates[date_obj]["n "+key]=nkprev+1
        self.dates[date_obj]["ms "+key]=((mskprev*nkprev)+tw_sent)/(nkprev+1)



    def whichkeys(self,tweet_text):
        """
        Returns which keys are in a text
        """
        found=[]
        for key in self.keywords:
            if key in tweet_text:
                found.append(key)
        return found

    def sent(self,text):
        """
        Analyse sentiment of text
        (so far only vader option)
        """
        scores=self.sid.polarity_scores(text)
        return scores['compound']



    def analyse_tweet(self,tweet):
        """
        Analyses a tweet and updates the statistics 
        of the corresponding day
        """
        #extract date
        dat=date_extract(tweet)
        #find type of tweet
        tw_typ=tweet_type(tweet)
        #extract text of tweet
        text=tweet_text(tweet,tw_typ)

        #find the keys of tweet:
        kys=self.whichkeys(text)

        if dat not in self.dates.keys():
            self.new_date(dat)

        for key in kys:
            #sentiment of tweet
            s=self.sent(text)
            self.update_stats(dat,key,s)

    





if __name__=="__main__":



    #uncompress selected raw sample
    raw_sample=GetTweets(5000)
    sample=Bytes_to_Json(raw_sample)

    A=TweetDayFrame()

    for x in sample:
        A.analyse_tweet(x)
    breakpoint()
