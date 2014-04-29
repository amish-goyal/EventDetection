import numpy as np

def jensenShannonDivergence(d1,d2):
  if len(d1) != len(d2):
    return None

  #Normalize
  d1 = d1/d1.sum()
  d2 = d2/d2.sum()
  
  average = [0.0 for i in range(len(d1))]
  for i in range(len(d1)):
    average[i] += (d1[i]+d2[i])/2

  return (klDivergence(d1,average)+klDivergence(d2,average))/2.0


def klDivergence(d1,d2):
  klDiv = np.double(0)
  for i in range(len(d1)):
    if d1[i] == 0:
      continue
    if d2[i] == 0.0:
      continue
    klDiv += d1[i] * np.log(d1[i]/d2[i])

  return klDiv/ np.log(2)

#d1 = [0.22,0.22,0.666]
#d2 = [0.232,0.099,0.4232]

#res = jensenShannonDivergence(d1,d2)

#print res
