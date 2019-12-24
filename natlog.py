from parser import parse
from unify import unifyWithEnv, extractTerm, \
   isvar,istuple,vars_of,const_of, has_vars,makeEnv

def ilen(it): sum(1 for x in it)

def refresh(l,t) :
  def ref(t) :
    if isvar(t) : return l+t
    elif not istuple(t) : return t
    else : return tuple(map(ref,t))
  return ref(t)

#def unfold(c,gs,vs) :
#  (h,bs)=c

def interp(css,goal) :
  def stats() :
    print('STATS','GS',len(gs),'VS',len(vs),'TR',len(trail))
  trail=[]
  gvars=vars_of(goal)
  print("GVARS",gvars)
  l0=len(gvars)
  vs=makeEnv(size=l0)
  print('VS0',vs)
  gs = list(goal)
  ppp("GS STARTING",gs,"\n")
  while gs :
    g=gs.pop()
    stats()
    #print("GOAL INTERP",extractTerm(g,vs),'\n')
    for (h0,bs0) in css :
      #print(h0,"BODY",bs0)
      l=len(vs)
      tl=len(trail)
      h=refresh(l,h0)
      print("YOUNGER", g, '<', l, '<', h)
      ok=unifyWithEnv(h,g,vs,trail,ocheck=True)

      if not ok :
        #print('FAIL', ok, 'G:', g,'<<<<<<', 'H:', h)
        for v in trail[tl:] :
          if v<l: vs[v]=v
          elif isvar(vs[v]) : ppp('VSV?????',vs[v])
        trail=trail[0:tl]
        print('VVVVVV',vs[:l+1])
        vs = vs[0:l]
        continue
      else :
        #print("NEW BODY", bs0)
        print('SUCC',g,'===>',extractTerm((g),vs))
        print('')
        for b0 in bs0:
          b=refresh(l,b0)
          gs.append(b)
          #print('APPENDING',b)
        #print('GS',gs)
        #print("GOAL !!!",goal,'==>\n\t',extractTerm(goal,vs),'\n')
  #print("VS!!!!",vs)
  yield extractTerm(goal,vs)


class natlog:
  def __init__(self,text):
    self.css=tuple(parse(text,ground=False,rule=True))
    #print(self.css)

  def query(self,quest):
    goal = tuple(parse(quest,ground=False,rule=False))
    print('GOAL PARSED',goal)
    for r in interp(self.css,goal) :
      print('ANSWER',r)

  def __repr__(self):
    xs = [str(cs) + '\n' for cs in self.css]
    return "".join(xs)

def natex() :
  text = """
      app () Ys Ys. 
      app (X Xs) Ys (X Zs) : 
          app Xs Ys Zs.

      nrev () ().
      nrev (X Xs) Zs : nrev Xs Ys, app Ys (X ()) Zs.
      """
  return natlog(text)

def ntest() :
  n=natex()
  print('DB')
  print(n)
  #n.query("app Xs Ys (a (b (c ())))?")
  #n.query("app (a (b ())) (c (d ())) R ?")
  n.query("nrev  (a (b (c (d ())))) R ?")

def ppp(*args) :print(*args)

if __name__ == '__main__':
  ntest()
