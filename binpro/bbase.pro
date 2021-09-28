% converts to/from bijective base B

fromBBase(_,[],0).
fromBBase(B,[D|Ds],NewN):-
  fromBBase(B,Ds,N),
  putBDigit(B,D,N,NewN).

toBBase(_,0,[]).
toBBase(B,N,[D|Ds]):-N>0,
  getBDigit(B,N,D,M),
  toBBase(B,M,Ds).

putBDigit(B,D,M,R):-D>=0,D < B, 
  R is 1+D+B*M.

getBDigit(B,N,Digit,NewN):-
  Q is N // B,
  D is N mod B,
  getBDigit1(D,Q,B,Digit,NewN).

getBDigit1(0,Q,B,Digit,NewN):-
  Digit is B-1,
  NewN is Q-1.
getBDigit1(D,Q,_B,Digit,Q):-D>0,
  Digit is D-1.
