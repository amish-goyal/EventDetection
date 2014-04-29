import pickle
import numpy as np  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

dir='lda_outputs/op-4hr1/'
TotalTopics=75
totalW=150

wtd=pickle.load(open(dir+'word_topic_dist.pkl'))
top_words=open(dir+'topics.txt').read().split('\n')[:TotalTopics]
topicwiseTweets=open(dir+'topic_tweetlist.txt').read().split('\n')[:-1]

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


def main():
    #filename = sys.argv[1]
    vocab=get_vocab()
    print "Vocab Size Considered: ",len(vocab)
    print "Creating Documents..."
    documents=treat_topic_as_doc(vocab)

    vectorizer = TfidfVectorizer(decode_error='ignore',min_df=1)
    x=vectorizer.fit_transform(documents)
    topic_tfidf_words={}

    feature_names=np.array(vectorizer.get_feature_names())
    xarray=x.toarray()
    for k in xrange(TotalTopics):
        print k
        topic_tfidf_words[str(k)]=list(feature_names[np.argsort(-xarray[k,:])][:20])    
    return topic_tfidf_words
    """
    tfidf = TfidfVectorizer(decode_error=u'ignore')
    tfs = tfidf.fit_transform(documents)



    tf_array = tfs.toarray() #Converting to numpy array

    doc_scores = {}
    for i,row  in enumerate(tf_array):
        cols = row.nonzero()
        for col in cols:
            doc_scores[documents[i]] = sum(tf_array[i][col])
    raw_input('Press enter to print results:')
    for item in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True):
        print "%f <= %s" % (item[1], item[0])
        raw_input('')
    """
dic=main()
    

"""
for k in xrange(1,TotalTopics):
    topTopicWords=top_words[k].split(' ')
    for i,idx in enumerate(np.argsort(-wtd[k])[:totalW]):
        print i,idx
        word=topTopicWords[i]
        prob=wtd[k,idx]
        print word, prob
        raw_input('')
"""