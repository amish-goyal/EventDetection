# Reads the mapped_topics file which contains the tweet mapped to the top 5 topics.
# Checks if a tweet has a topic with prob > 0.9 and which topic is it. If there is no such topic, then throw the tweet.
# OUTPUTS: tweet_flat_topic.text -- tweets which are thrown because they do not satisfy the 0.9 threshold
# OUTPUTS: tweet_thresholdtopic.text -- tweets which satisfy the threshold condition
# OUTPUTS: topic_tweetlist -- topic# followed by tweets which belong to that topic 

# INPUT: tweets with segments in file -- ../../OVERALL-inject-150k-it300-t25/input/20090611_1.text
# INPUT: tweets without segments in --- ../tweets_noneng/20090611.text ##-- TO BE USED LATER --##
# INPUT: mapped_topic.text -- file containing topic# of the top 5 topics assigned to each tweet from file ../../OVERALL-inject-150k-it300-t25/input/20090611_1.text 

import pickle
from collections import defaultdict

TotalTopics=75
ip='inputFiles/tweets_4hrs_2.txt'
datapkl='inputPkls/tweets4hrs2.pkl'
op='lda_outputs/op-4hr2/'

#tweets=open('./input/20090611_1.text','r').read().split('\n')
#tweets_nosegs=open('../tweets_noneng/20090611.text','r').read().split('\n')
tweets=open(ip,'r').read().split('\n')
topics=open(op+'mapped_topics.txt','r').read().split('\n\n\n')
f=open(op+'tweet_topic_dist.pkl','rb')
ftopic_passthreshold = open(op+'tweet_thresholdtopic.txt','w')
ftopic_flat = open(op+'tweet_flat_topic.txt','w')
ftopic_tweets = open(op+'topic_tweetlist.txt','w')
data = pickle.load(open(datapkl))
newdatapkl = open(op+'js.pkl','w')
newdata={}
t=pickle.load(f)
f.close()
count=0
print "unpickled!"

topic_tweets = defaultdict(list)
datakeys=data.keys()
print "Total keys in dictionary: ",len(datakeys)
print "Total rows in the distribution: ",t.shape[0]

for i in range(t.shape[0]):
    for k in range(TotalTopics): #Check which topic is it? 
        flag=0
        if(t[i,k]) > 0.9:
            topic_tweets[k] += [tweets[i]] #topic_tweets is a dict with topic# : [list of tweets in that topic]
            if tweets[i] != data[str(i)]['tok-tweet']:
                print tweets[i]
                print data[str(i)]
                raw_input("Error: Tweet and dictionary value do not match!")
            count+=1
            data[str(i)]['topic']=str(k)
            newdata[str(i)]=data[str(i)]
            flag=1
            ftopic_passthreshold.write(str(tweets[i])+'\n')
            continue
        if flag==0:
            data[str(i)]['topic']='flat'
        
print count

#Save topics and list of tweets in each topic in a file
for topic_num in topic_tweets.keys():
    tweet_list = topic_tweets[topic_num]
    for tweet in tweet_list:
        ftopic_tweets.write('topic'+str(topic_num)+' '+tweet+'\n')
pickle.dump(newdata,newdatapkl)
newdatapkl.close()
"""
out of the 433173 tweets, 301556 have a non flat distribution
"""
