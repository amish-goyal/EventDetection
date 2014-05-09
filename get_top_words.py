"""
This script writes the top words according to the topic word distribution output by LDA to a file named top-words.txt
The variables that need to be set before running the script are dir (the path of the LDA output dir), TotalTopics, totalW
"""

import pickle
import numpy as np
#voca,lda=pickle.load(open('model.dat'))

dir='lda_outputs/css/'
TotalTopics=35
totalW=15

wtd=pickle.load(open(dir+'word_topic_dist.pkl'))

tws=open(dir+'topics.txt').readlines()
with open(dir+'top-words.txt','w') as f:
    for k in xrange(TotalTopics):
        f.write('TOPIC: %d+ \n' %(k))
        for word in tws[k].split(' ')[:totalW]:
            f.write(word+'\n')
        f.write('\n\n')
"""
with open('top15.txt','w') as f:
    for k in xrange(75):
        f.write("TOPIC: %d" %(k))
        for w in np.argsort(-wtd[k])[:15]:
            f.write(voca[w])
        f.write("\n")
"""
