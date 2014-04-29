import pickle
import numpy as np
#voca,lda=pickle.load(open('model.dat'))

dir='lda_outputs/css/'
TotalTopics=35

wtd=pickle.load(open(dir+'word_topic_dist.pkl'))

tws=open(dir+'topics.txt').readlines()
with open(dir+'top15-2.txt','w') as f:
    for k in xrange(TotalTopics):
        f.write('TOPIC: %d+ \n' %(k))
        for word in tws[k].split(' ')[:15]:
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
