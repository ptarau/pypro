from .db import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

#from answerer import tsv2mat
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# it might work better for larger databases
def_learner=MLPClassifier(
  hidden_layer_sizes=(16,16),
  #random_state=1234,
  verbose=1,
  activation='relu',
  max_iter=10000
)

#def_learner=RandomForestClassifier(random_state=1234)

def set2bits(n,xs) :
  return [1 if x in xs else 0  for x in range(n)]

def bits2set(bs):
  return [i for i,b in enumerate(bs) if b==1]

def seq2nums(xs) :
  d=dict()
  i=0
  for x in xs :
    if x not in d:
      d[x]=i
      i+=1
  return d

def num2bits(l,n) : # binary encoding
  #return [n] # no encoding
  blen=len(bin(l)[2:])
  cs=bin(n)[2:]
  r=blen-len(cs)
  bs=r*[0]+[int(c) for c in cs]
  #return bs # binary encoding
  return set2bits(l, [n]) # 1hot encoding


class ndb(db) :

  def load(self,fname,learner=def_learner):
    super().load(fname)

    db_const_dict = seq2nums(self.index)
    db_const_count=len(db_const_dict)
    bss=[]
    for n in db_const_dict.values() :
      bs=num2bits(db_const_count,n)
      bss.append(bs)
    X=np.array(bss)
    #X=np.eye(len(db_const_dict),dtype=int)

    val_count = len(self.css)
    y = np.array([set2bits(val_count, xs) for xs in self.index.values()])
    print('X:',X.shape,'\n',X)
    print('\ny:',y.shape,'\n',y,'\n')
    learner.fit(X,y)

    self.learner,self.db_const_dict,self.y = learner,db_const_dict,y

  def ground_match_of(self,query_tuple):

    query_consts = const_of(query_tuple)
    query_consts_nums = \
      [self.db_const_dict[c] for c in query_consts if c in self.db_const_dict]
    db_const_count = len(self.db_const_dict)
    rs = np.array([[1] * self.y.shape[1]])
    '''
    for qn in query_consts_nums:
      qa = np.array([[q for q in num2bits(db_const_count, qn)]])
      r = self.learner.predict(qa)
      #print('PROBS',self.learner.predict_proba(qa))
      rs = np.bitwise_and(rs, r)
    '''
    qas= np.array([set2bits(db_const_count,query_consts_nums)])
    #print('QQQQ',qas)
    rs = self.learner.predict(qas)

    matches = list(rs[0])
    matches = bits2set(matches)
    #print('matches:', matches)
    return matches


