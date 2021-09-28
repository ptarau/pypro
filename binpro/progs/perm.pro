goal(X):-perm([aa,bb,cc,dd],X).

perm([],[]).
perm([X|Xs],Zs):-
  perm(Xs,Ys),
  ins(X,Ys,Zs).
  
ins(X,Xs,[X|Xs]).
ins(X,[Y|Xs],[Y|Ys]):-ins(X,Xs,Ys).

%goal(X):-ins(aa,[bb,cc],X).
