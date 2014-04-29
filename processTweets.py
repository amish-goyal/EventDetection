"""
This script generates files containing tweets within a particular time window.

PARAMETERS:
filenames: list of json files to read the raw tweets from
total_windows: no of time windows to be considered
window_size: size of each time window in hours

Location of generated files:
inputFiles: contains txt files with tweets
inputPkls: contains corresponding pickled dictionaries that contain the tweet metadata
"""

import json
from datetime import datetime as dt
import datetime
import pickle
import string
from nltk.stem.porter import PorterStemmer as ps


dir="/nethome/tmitra3/quac/tweets/2014-02/"
filenames=["20140227_194156.json","20140227_215708.json","20140228_001137.json","20140228_032352.json","20140228_053717.json","20140228_070209.json","20140228_090631.json","20140228_105638.json","20140228_130315.json","20140228_153108.json","20140228_175055.json","20140228_200714.json","20140228_222308.json"]

total_windows=2
window_size=4

def read_tweets():
    global dir,filenames
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
                        yield info["id_str"],info["text"].encode('utf-8').replace('\n',' '),info["created_at"],"",info["lang"]

                except Exception,e:
                    pass
                    #print e
                    #count+=1
                    #print count

def get_time(time):
    return dt.strptime(time.split(' ')[3],"%H:%M:%S")

def tok_tweet(tweet):
    stemmer=ps()
    tweet = tweet.strip()
    words = tweet.split()
    tokenlist = []
    exclude = set(string.punctuation)
    punc = string.punctuation
    punc = punc.replace('#','') #we have speical handling for #tag
    exclude_punc = set(punc)
    for word in words:
        word = word.strip()
        word = word.lower()
        #Replace URLs with @http and then with blank -- think about this later (phase2)
        if word.startswith('www') or word.startswith('http') or word.startswith("@") or word.isdigit():
            continue #ignore if word is a url, @mention or contains only numbers or is a stopword
        if ''.join(ch for ch in word if ch not in exclude) == '': #remove word if it is a sequence of punctuation characters
            continue
        nword = ''.join(ch for ch in word if ch not in exclude_punc)
        tokenlist.append(stemmer.stem(nword))
    tokens= tokenlist
    return ' '.join(tokens)
        
def add_tweet_data(tweet,tokTweet,time,name,tid):
    dic={}
    dic["raw-tweet"]=tweet
    dic["tok-tweet"]=tokTweet
    dic["time"]=time
    dic["name"]=name
    dic["ID"]=tid
    return dic

def generate_oneFile(reader,window_no):
    global window_size,total_windows
    outfile = 'inputFiles/tweets_%dhrs_%d.txt' %(window_size,window_no)
    pklfile = 'inputPkls/tweets%dhrs%d.pkl' %(window_size,window_no)

    data={}
    tweets=[]
    with open(outfile,'w') as f:
        count=-1
        
        tid,tweet,start,name,lang = reader.next()
        start_time=get_time(start)
        print 'Time of First tweet: ',start_time

        for tid,tweet,time,name,lang in reader:
            if lang=='en':
                tokTweet=tok_tweet(tweet)
                count+=1

                if count%10000==0:
                    print "Tweets Processed: %d" %(count)
                f.write(tokTweet)
                f.write('\n')

                data[str(count)]=add_tweet_data(tweet,tokTweet,time,name,tid)
                
                assert count+1==len(data)
                    
                if get_time(time)-start_time>datetime.timedelta(0,3600*window_size):
                    with open(pklfile,'w') as pf:
                        pickle.dump(data,pf)
                    f.close()
                    break
        return count

def generate_LDA_input_files():
    global total_windows
    reader=read_tweets()
    for i in xrange(total_windows):
        print "Window No.: ",i+1
        tweetCount=generate_oneFile(reader,i+1)
        print "Total English Tweets: %d" %(tweetCount)

generate_LDA_input_files()
