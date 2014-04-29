"""
This file requires the following parameters:
dir: the path of the folder containing the tweets in json format
filenames: the names of json files present in the 'dir' folder
total_windows: total number of time windows to be analyzed
window_size: size of one time window in hours
"""

import json
from datetime import datetime as dt
import datetime
import pickle
import string
from nltk.stem.porter import PorterStemmer as ps


dir="/nethome/tmitra3/quac/tweets/2014-02/"

filenames=["20140227_194156.json","20140227_215708.json","20140228_001137.json","20140228_032352.json","20140228_053717.json","20140228_070209.json","20140228_090631.json","20140228_105638.json","20140228_130315.json","20140228_153108.json","20140228_175055.json","20140228_200714.json","20140228_222308.json"]

total_windows=8

window_size=4

def read_tweets():
    count=0
    global filenames
    test=0
    for filename in filenames:
        with open(dir+filename) as infile:
            data=infile.read()
            raw_tweets=data.split('\n')
            for tweet in raw_tweets:
                try:
                    info=json.loads(tweet)
                    
                    if "screen_name" in info["user"]:
                        #print info["user"]["screen_name"]
                        #raw_input("")
                        yield info["id_str"],info["text"].encode('utf-8').replace('\n',' '),info["created_at"],info["user"]["screen_name"],info["lang"]
                    else:
                        yield info["id_str"],info["text"].encode('utf-8').replace('\n',' '),info["created_at"],"",info["lang"]#,info["entitites"]["hashtags"]

                except Exception,e:
                    pass
                    #print e
                    #count+=1
                    #print count


def get_time(time):
    return dt.strptime(time.split(' ')[3],"%H:%M:%S")        

def get_tweets_window(reader):
    global window_size
    tc=0
    eng_tc=0
    tid,tweet,start,name,lang = reader.next()
    start_time=get_time(start)
    print "\nTime Stamp starts at: ", start_time
    for tid,tweet,time,name,lang in reader:
        tc+=1
        if lang=='en':
            eng_tc+=1
        if get_time(time)-start_time>datetime.timedelta(0,3600*window_size):
            return tc,eng_tc
        
    """
    with open('tweets-3hr-2.txt','w') as f:
        start,_ = reader.next()
        start_time=get_time(start)
        print start_time
        for time,tweet in reader:
            f.write(tweet.encode('utf8'))
            f.write('\n')
            if get_time(time)-start_time>datetime.timedelta(0,1800*6):
                break
    """


tweets=[]
engtweets=[]
def get_stamp_sizes():
    global tweets,engtweets,total_windows
    reader=read_tweets()
    for i in xrange(total_windows):
        tc,eng_tc=get_tweets_window(reader)
        print "Window No.: ",i
        print "Total Tweets: %d, Total English Tweets: %d" %(tc,eng_tc)
        tweets.append(tc)
        engtweets.append(eng_tc)

def plot_time_stamp_sizes():
    import matplotlib.pyplot as plt 
    global tweets,engtweets
    plt.plot()

get_stamp_sizes()

