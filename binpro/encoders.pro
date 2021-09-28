term2paths(T,Pss):-
   findall(Ps,term2path(T,Ps),Pss).


term2path(T,Ps):-term2path(T,[],Ps).

term2path(T,Ps,[I|NewPs]):-
   compound(T),
   !,
   argx(I,T,X),
   term2path(X,Ps,NewPs).
term2path(A,Ps,[A|Ps]).

argx(0,T,F):-functor(T,F,_).
argx(I,T,F):-arg(I,T,F).

:-op(100,xfy,('=>')).
etest:-
  %T=f(a,g(b,h(c),d),e),
  T=((_=>A=>'[|]')=>(_=>B=>'[|]')=>C=>gen_places :-
    A=>B=>C=>gen_places
),
  writeln(T),
  term2paths(T,Pss),
  writeln(Pss),
  fail.

