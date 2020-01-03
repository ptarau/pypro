# immutable list emulation
from .unify import istuple

def genList(n) :
  return fromList(range(n))

def fromList(Xs) :
  Rs=()
  for X in reversed(Xs) :
    Rs=X,Rs
  return Rs

def toGen(As) :
  while As != () :
    A,As=As
    yield A

def toList(As) : return list(toGen(As))

def concat(As,Cs):
  if As == ()  : return Cs
  assert isCons(As)
  A,Bs=As
  return A,concat(Bs,Cs)

def llen(As) :
  if As == () : return 0
  else :
    _,Bs=As
    return 1+llen(Bs)

def lshow(As) :
  for A in toGen(As) :
    print('  ',A)

def isCons(As) :
  return istuple(As) and len(As)==2

def isLList(As) :
  if As == () : return True
  elif  isCons(As):
    _,Bs=As
    return isLList(Bs)
  else:
    return False

# def cons(A,B) : return (A,B)
