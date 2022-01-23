from .natlog import natlog
from .db import db
from .unify import const_of

#from Natlog.Parser import parse
#from Natlog.Scanner import Int
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

#from answerer import tsv2mat
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# WORK IN PROGRESS, TODO "

def tsv2db(fname='natprogs/Db.tsv'):
  rels=db()
  #wss = tsv2mat(fname)
  #for ws in wss: rels.add_db_clause(ws)
  rels.load_tsv(fname)
  return rels

'''
def wss2hotXy(wss,io_split = -1) :
  Xy=np.array(wss)
  X=Xy[:,:io_split]
  y=Xy[:,io_split:]
  print(X.shape,y.shape)

  enc=OneHotEncoder(handle_unknown='ignore')
  enc.fit(X)
  hotX=enc.transform(X).toarray()

  enc_ = OneHotEncoder(handle_unknown='ignore')
  enc_.fit(y)
  hoty = enc_.transform(y).toarray()

  #print(hotX.shape,hoty.shape)
  #coldX=enc.inverse_transform(hotX)
  #print(coldX[0])
  return enc,hotX,enc_,hoty
'''

def wss2hotX(wss,mask) :
  mask=[mask]*len(wss[0])
  X=np.array(wss)
  Xplus=np.array(wss+[mask])
  print(Xplus.shape)
  enc=OneHotEncoder(handle_unknown='ignore')
  enc.fit(X)
  hotX=enc.transform(X).toarray()
  return enc,X,hotX


# it might work for larger databases
learner=MLPClassifier(
  hidden_layer_sizes=(64,16,64),
  verbose=True,
  activation='logistic',
  max_iter=10000)

learner=RandomForestClassifier(random_state=1234)

# bit encodings

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


class multilearner(natlog) :
  def __init__(self,
               text=None,
               file_name=None,
               tsv_file='natprogs/Db.tsv',
               learner=learner
               ):
    if not text and not file_name: text = ""
    super().__init__(text=text, file_name=file_name)
    self.learner = learner
    self.rels = tsv2db(fname=tsv_file)
    l=len(self.rels.css)

    ixbits=dict((x,set2bits(l,xs)) for (x,xs) in self.rels.index.items())
    codes=seq2bits(self.rels.index)
    print(len(ixbits),len(codes))
    #print(ixbits)
    X=np.array(codes)
    y=np.array(list(ixbits.values()))
    print(X)
    print('\n',y)
    self.X,self.y,self.codes,self.ixbits=X,y,codes,ixbits
    self.train()

  def generator_transformer(self):
    print("!!!!!!THERE")

    def eval_it(x):
      print('EVAL', x, type(x))
      f = eval(x)
      print('AFTER EVAL', f, type(f))
      return f

  def train(self):
    self.learner.fit(self.X,self.y)


  def ask(self,qs):
    print('TODO')
    names_nums = seq2nums(self.rels.index)
    consts=const_of(qs)
    #print('NAMES',names_nums)
    #print('CONSTS',consts)
    nums=[names_nums[c] for c in consts if c in names_nums]
    #print('NUMS',nums)
    l=len(names_nums)
    rs=np.array([[1]*self.y.shape[1]])
    for qn in nums :
      qa=np.array([[q for q in set2bits(l,[qn])]])
      r=self.learner.predict(qa)
      rs=np.bitwise_and(rs,r)
    #print('RRR',rs[0])
    vals=list(rs[0])
    vals=list(bits2set(vals))
    print('VALS:',vals)
    Ans=[self.rels.css[v] for v in vals]
    for A in Ans: yield A


'''
class natlearner(Natlog) :
  def __init__(self,
               text=None,
               file_name=None,
               tsv_file='natprogs/Db.tsv',
               learner=learner
               ):
    if not text and not file_name : text = ""
    super().__init__(text=text,file_name=file_name)
    self.learner = learner
    self.mask='###'
    self.rels=tsv2db(fname=tsv_file)
    self.y0=np.array(self.rels.css)
    self.enc,self.X,self.hotX=wss2hotX(self.rels.css,self.mask)
    
  def train(self):
    width=self.y0.shape[1]

    yargs=[self.hotX for _ in range(width)]
    y=np.concatenate(yargs,axis=0)

    maskColumn=np.array([self.mask]*self.X.shape[0])

    xargs=[]
    for i in range(width) :
      Xi=self.X.copy()
      Xi[:,i]=maskColumn
      xargs.append(Xi)

    X=np.concatenate(tuple(xargs),axis=0)
    X=self.enc.transform(X)

    print(X.shape,y.shape)
    return self.learner.fit(X,y)

  def ask(self,qss):
    Q=np.array(qss)


    hotQ=self.enc.transform(Q).toarray()

    assert hotQ.shape[1]==self.hotX.shape[1]

    hotA=(self.learner.predict(hotQ))

    altA = (self.learner.predict_proba(hotQ))

    for x in hotA[0]: print('$$$',x)

    for x in altA: print('!!!', x)



    #print("\nANSWER's hot shape",hotA.shape,'\n')

    A=self.enc.inverse_transform(hotA)

    return A
'''



