/*
Program:  MUSIC MEN Puzzle
Author:   Paul Tarau
Date:     August 1992

MUSIC MEN

Three friends like different kinds of music.  From the clues given
below, can you identify them, say how old each is, and work out
his musical preference?

Clues: 
1.      Rob is older than Queen, who likes classical music.
2.      The pop-music fan, who is not Prince, is not 24.
3.      Leon, who is not King, is 25.
4.      Mark's musical preference is not jazz.

Knowledge: "this is what we know of the world."
Names           : Leon, Mark, Rob.
Surnames        : King, Prince, Queen.
Ages            : 24, 25, 26.
Music           : Classical, Jazz, Pop.

% solution

Leon Prince, 25, jazz.
Mark Queen, 24, classical.
Rob King, 26, pop.
*/

% Well, I simply cannot resist to so much music and royalty...

solve(D0):-
	data(D0),

	% 1.      Rob is older than Queen, who likes classical music.
	older(RAge,QAge),
	pick(D0,D1,_,[queen,QAge,classic]),
	pick(D1,_,rob,[_,RAge,_]),

	% 2.      The pop-music fan, who is not Prince, is not 24.
	pick(D0,E1,_,[_,_,pop]),
	pick(E1,E2,_,[prince,_,_]),
	pick(E2,_,_,[_,24,_]),

	% 3.      Leon, who is not King, is 25.
	pick(D0,F1,leon,[_,25,_]),
	pick(F1,_,_,[king,_,_]),

	% 4.      Mark's musical preference is not jazz.
	pick(D0,G1,mark,[_,_,_]),
	pick(G1,_,_,[_,_,jazz]).

older(26,25).
older(25,24).
older(26,24).
	
data([	
	[_-king,_-prince,_-queen],	% surnames
	[_-24,_-25,_-26],		% ages
	[_-classic,_-jazz,_-pop]	% musical preferences
]).

sel(X,[X|Xs],Xs).
sel(X,[Y|Xs],[Y|Ys]):-sel(X,Xs,Ys).

pick([],[],_,[]).
pick([Xs|Xss],[Ys|Yss],Name,[A|As]):-
	sel(Name-A,Xs,Ys),
	pick(Xss,Yss,Name,As).

goal(X):-solve(X).
