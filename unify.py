# unification algorithm
# compound terms are tuples, variables are denoted with ints
# use strings, floats etc. for constants, and numeric data !!!
# if you need ints, wrap them as Ints

# extracts if after unification succeeds
def  unifyToTerm(x1,x2) :
  vs = makeEnv()
  if unifyWithEnv(x1,x2,vs) :
    t1 = extractType(x1,vs)
    t2 = extractType(x2,vs)
    #print (t1,'==',t2)
    return t1
  else :
    return None

# unifies, returning the envoronment with bindings    
def  unifyToEnv(x1,x2) :
  vs = makeEnv()
  if unifyWithEnv(x1,x2,vs) : return vs
  else : return None

# contains list of bindings
def makeEnv(size=0) :
  if size : return list(range(size))
  return []

def extendTo(n,vs) :
  for i in range(len(vs),n+1) :
    vs.append(i)
  return vs

# builds a term following bindings in environment. es      
def extractType(x,es) : 
  def et(x) :
    t = deref(x,es)
    if isvar(t) : return t
    elif not istuple(t) : return t
    else : return tuple(map(et,t))
  return et(x)

# unifies, by extending given environment vs
def unifyWithEnv(x1,x2,vs) :
  t1 = deref(x1,vs)
  t2 = deref(x2,vs)
  b1 = isvar(t1)
  b2 = isvar(t2)
  if b1 and b2 :
    if t1 != t2 : 
      i,j = max(t1,t2),min(t1,t2)
      vs[i]=j
    return True
  elif b1:
    return bind(t1,t2,vs)
  elif b2 :  
    return bind(t2,t1,vs)
  elif not istuple(t1) :
    return t1==t2
  else :
    n1 = len(t1)
    n2 = len(t2)
    if n1 != n2 : return False
    for i in range(n1) :
      if not unifyWithEnv(t1[i],t2[i],vs) : return False
    return True

# occurs check, for sound unification  
def occurs(j,t,vs) :
  i = deref(j,vs)
  s = deref(t,vs)
  return occurs1(i,s,vs)
     
def occurs1(i,t,vs) :
  if isvar(t) : return i==t
  elif not istuple(t) : return False
  else :
    for s in t :
      if occurs(i,s,vs) : return True
    return False

# vars are just ints 
def isvar(i) : return isinstance(i,int)

# compound terms are tuples
# no special role for first arguments

def istuple(t) : return isinstance(t,tuple)

# follows variables references to unbound var or nonvar     
def deref(i,vs) :
  if not isvar(i) :return i
  if i >= len(vs): extendTo(i, vs)
  while(isvar(i)) :
    j = vs[i]
    if i == j : break
    i = j
  return i

# binds var to term  
def bind(i,t,vs) :
  if occurs1(i,t,vs) : return False
  else :
    vs[i]=t
    return True


# tests        
   
t1 = (((1,1),(2,1)),(1,2))
t2 = ((5,6),7)
t3 = ((0,1),1)
t4 = (2,2)

vs1 = [0,1,1,2,0]

def test1() :
  return [occurs(2,t1,vs1),occurs(3,t1,vs1),occurs(0,t1,vs1),occurs(4,t1,vs1)]
    
def test2() :
  print(t1,'=',t2)
  print(unifyToEnv(t1,t2))
  print(unifyToTerm(t1,t2))
  print(unifyToEnv(t3,t4))
  
tt1 = (((1,1),(2,1)),(1,2),1)
tt2 = ((5,6),7,8)
tt3 = ((0,1),1,2)
tt4 = (3,4,4)


def test3() :
  print(tt1,'=',t2)
  print(unifyToEnv(tt1,tt2))
  print(unifyToTerm(tt1,tt2))
  print(unifyToEnv(tt3,tt4))

X=0
Y=1
Z=2
U=3

def f(x,y,z) : return ('f',x,y,z)

def g(x,y) :return ('g',x,y)

a='a'
b='b'

u1=f(U,g(X,X),g(Y,Y))
u2=f(b,g(a,Y),Z)

def utest() :
  print(u1,'=',u2)
  print(unifyToEnv(u1, u2))
  print(unifyToTerm(u1,u2))

if __name__=='__main__' :
  utest()
   
