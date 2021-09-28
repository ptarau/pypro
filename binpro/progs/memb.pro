eq(X,X).

memb(X,[X|_]).
memb(X,[_|Xs]):-memb(X,Xs).

goal(X):-memb(Y,[aa,bb,cc]),eq(X,Y).
