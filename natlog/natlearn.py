from .natlog import natlog
from .db import db
#from natlog.parser import parse
#from natlog.scanner import Int
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

#from answerer import tsv2mat
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# WORK IN PROGRESS, TODO "

def tsv2db(fname='natprogs/db.tsv'):
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

'''
# it might work for larger databases
learner=MLPClassifier(
  hidden_layer_sizes=(16,16,16),
  verbose=True,
  activation='logistic',
  max_iter=1000)
'''
learner=RandomForestClassifier(random_state=1234)

class natlearner(natlog) :
  def __init__(self,
               text=None,
               file_name=None,
               tsv_file='natprogs/db.tsv',
               learner=learner
               ):
    if not text and not file_name : text = ""
    super().__init__(text=text,file_name=file_name)
    self.mask='###'
    self.rels=tsv2db(fname=tsv_file)
    self.y0=np.array(self.rels.css)
    self.enc,self.X,self.hotX=wss2hotX(self.rels.css,self.mask)
    self.learner=learner

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

    print("\nANSWER's hot shape",hotA.shape,'\n')

    A=self.enc.inverse_transform(hotA)

    return A




