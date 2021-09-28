goal(ok):-loop.

%step(X,X).

%loop(_).
%loop(X):-step(X,Y),loop(Y).

%goal(ok):-loop(aa).
%loop.
%loop:-loop.

step.

loop.
loop:-step,loop.
