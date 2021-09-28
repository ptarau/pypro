% this generates the 288 puzzles
% and solves one if given clues
/*
sudoku(Xss):-
 s4x4(Xsss),Xsss=[Xss|_],
 maplist(maplist(permute([1,2,3,4])),Xsss).
*/

% exam solution here

sudoku(Xss):-
 s4x4(Xsss),eq(Xsss,[Xss|_]),
 fill_out_blocks(Xsss).
 
fill_out_rows([]).
fill_out_rows([P|Ps]):-
	permute([1,2,3,4],P),
	fill_out_rows(Ps).
 
fill_out_blocks([]).
fill_out_blocks([B|Bs]):-
	 fill_out_rows(B),
	 fill_out_blocks(Bs).

eq(X,X).

s4x4([
 [
    [S11,S12, S13,S14],
    [S21,S22, S23,S24],

    [S31,S32, S33,S34],
    [S41,S42, S43,S44]
 ],
 [
    [S11,S21, S31,S41],
    [S12,S22, S32,S42],

    [S13,S23, S33,S43],
    [S14,S24, S34,S44]
 ],
 [
    [S11,S12, S21,S22],
    [S13,S14, S23,S24],

    [S31,S32, S41,S42],
    [S33,S34, S43,S44]
 ]
]).
% here you can add clues like S11=3, S41=2, etc.
% tested with SWI-Prolog - uses maplist/2


permute([],[]).
permute([X|Xs],Zs):-permute(Xs,Ys),ins(X,Ys,Zs).

ins(X,Xs,[X|Xs]).
ins(X,[Y|Xs],[Y|Ys]):-ins(X,Xs,Ys).

% test
goal(Sol):-sudoku(Sol).
