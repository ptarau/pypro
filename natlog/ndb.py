from .db import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

#from answerer import tsv2mat
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# it might work for larger databases
def_learner=MLPClassifier(
  hidden_layer_sizes=(64,16,64),
  verbose=True,
  activation='logistic',
  max_iter=10000)

def_learner=RandomForestClassifier(random_state=1234)


def wss2hotX(wss,mask) :
  mask=[mask]*len(wss[0])
  X=np.array(wss)
  Xplus=np.array(wss+[mask])
  print(Xplus.shape)
  enc=OneHotEncoder(handle_unknown='ignore')
  enc.fit(X)
  hotX=enc.transform(X).toarray()
  return enc,X,hotX

def set2bits(n,xs) :
  return tuple(1 if x in xs else 0  for x in range(n))

def bits2set(bs):
  return (i for i,b in enumerate(bs) if b==1)

def seq2nums(xs) :
  return dict((x,i) for (i,x) in enumerate(xs))

def seq2bits(xs) :
  d=seq2nums(xs)
  l=len(xs)
  return tuple(set2bits(l,[d[x]]) for x in xs)

def bits2seq(xs,bss) :
  nss = map(bits2set,bss)
  return [xs[i] for ns in nss for i in ns]

class ndb(db) :

  def load(self,fname,learner=def_learner):
    print("load OVERRRIDE")
    super().load(fname)
    l = len(self.css)
    self.learner=learner

    ixbits=dict((x,set2bits(l,xs)) for (x,xs) in self.index.items())
    codes=seq2bits(self.index)
    print('DIMS',len(ixbits),len(codes))
    X=np.array(codes)
    y=np.array(list(ixbits.values()))
    print(X)
    print('\n',y)
    self.X,self.y,self.codes,self.ixbits=X,y,codes,ixbits
    self.learner.fit(self.X,self.y)


  def ground_match_of(self,h):
    #print("ground_match_of OVERRRIDE")
    names_nums = seq2nums(self.index)
    consts = const_of(h)
    nums = [names_nums[c] for c in consts if c in names_nums]
    # print('NUMS',nums)
    l = len(names_nums)
    rs = np.array([[1] * self.y.shape[1]])
    for qn in nums:
      qa = np.array([[q for q in set2bits(l, [qn])]])
      r = self.learner.predict(qa)
      rs = np.bitwise_and(rs, r)
    # print('RRR',rs[0])
    vals = list(rs[0])
    vals = list(bits2set(vals))
    #print('VALS:', vals)
    return vals


