collect_leaf(v(Leaf),Leaf).
collect_leaf([X|_],Leaf):-collect_leaf(X,Leaf).
collect_leaf([_|Xs],Leaf):-collect_leaf(Xs,Leaf).

goal(L):-collect_leaf([[v(a),[v(b)],v(X)],[v(X),v(e),[]]],L).

