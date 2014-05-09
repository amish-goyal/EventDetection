"""
To run this script, enter the path of the LDA output directory.
The variable totalW selects the count of top words from each topic to generate a new vocabulary
The variable ImpWords selects the no. of relevant words to be output for each topic
The TotalTopics variable needs to be set to the total topic configuration set for running LDA

The output of the script is a dictionary that contains the top relevant words for each topic
"""

import pickle
import numpy as np  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

dir='lda_outputs/op-4hr2/'
lamda=0
TotalTopics=75
totalW=150
ImpWords=30

wtd=pickle.load(open(dir+'word_topic_dist.pkl'))
top_words=open(dir+'topics.txt').read().split('\n')[:TotalTopics]
topicwiseTweets=open(dir+'topic_tweetlist.txt').read().split('\n')[:-1]
#corpus=open(dir+'topic_tweetlist.txt').read()
allvocab=pickle.load(open(dir+'vocab.pkl'))

def get_vocab():
    vocab=[]
    for k in xrange(TotalTopics):
        topTopicWords=top_words[k].split(' ')[:totalW]
        vocab+=topTopicWords
    return set(vocab)

def treat_topic_as_doc(vocab):
    documents=['']*TotalTopics
    for tweet in topicwiseTweets:
        topic_no=int(tweet.split()[0][5:])
        documents[topic_no]+=' '.join(list(set(tweet.split()) & vocab))+' '
    return documents

def get_word_dist_matrix(vocab_subset):
    word1=vocab_subset[0]
    word_dist=wtd[:,allvocab.index(word1)]
    
    for word in vocab_subset[1:]:
        word_dist=np.column_stack((word_dist,wtd[:,allvocab.index(word)]))
    return word_dist

def get_freq_based_matrix():
    vocab=get_vocab()
    print "Vocab Size Considered: ",len(vocab)
    print "Creating Topic Documents..."
    documents=treat_topic_as_doc(vocab)
    #corpus=' '.join(documents)
    print "Running CountVectorizer..."
    vectorizer = CountVectorizer(decode_error='ignore',min_df=0,vocabulary=vocab)#stop words??
    x=vectorizer.fit_transform(documents).toarray()
    return x,vectorizer.get_feature_names()
    
def get_relavant_word_dict(lamda=0):
    b,feature_names=get_freq_based_matrix()
    a=get_word_dist_matrix(feature_names)
    b=a/b#(np.tile(np.sum(b,axis=0),(TotalTopics,1)))
    relevance_matrix = lamda*a+(1-lamda)*b
    vocab=np.array(feature_names)
    topic_relevant_words={}
    for k in xrange(TotalTopics):
        subset=np.argsort(-relevance_matrix[k,:])
        topic_relevant_words[str(k)]=list(vocab[subset][:ImpWords])
    return topic_relevant_words


def main():
    global lamda
    topicwise_relavant_words=get_relavant_word_dict(lamda)
    return topicwise_relavant_words
    
dic=main()



