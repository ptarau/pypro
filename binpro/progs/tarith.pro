goal(X):-four(A),mul(A,A,B),add(B,B,X). %32

eq(X,X).

add(e,X,X).
add(SX,Y,SZ):-p(SX,X),add(X,Y,Z),s(Z,SZ).

mul(e,_,e).
mul(SX,Y,Z):-p(SX,X),mul(X,Y,T),add(Y,T,Z).

four(X):-s(e,A),s(A,B),s(B,C),s(C,X).

s(e,c(e,e)).
s(c(e,Y),V):-s(Y,A),q(A,V).
s(Z,c(e,A)):-r(Z,A).

q(c(A,B),c(R,B)):-s(A,R).

r(c(A,B),c(R,B)):-p(A,R).

p(c(e,e),e).
p(c(e,Y),R):-q(Y,R).
p(Z,c(e,R)):-r(Z,A),p(A,R).
