eq(X,X).

add(0,X,X).
add(s(X),Y,s(Z)):-add(X,Y,Z).

mul(0,_,0).
mul(s(X),Y,Z):-mul(X,Y,T),add(Y,T,Z).

goal(R):-eq(X,s(s(s(0)))),mul(X,X,Y),add(A,B,Y),eq(R,sum(A,B)).

