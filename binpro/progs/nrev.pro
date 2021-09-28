goal(Zs):-nrev([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],Zs).

nrev([],[]).
nrev([X|Xs],Zs):-nrev(Xs,Ys),app(Ys,[X],Zs).

app([],Ys,Ys).
app([X|Xs],Ys,[X|Zs]):-app(Xs,Ys,Zs).

%goal(Xs):-app([1,2,3],[4,5],Xs).

%goal([Xs,Ys]):-app(Xs,Ys,[1,2,3]).
