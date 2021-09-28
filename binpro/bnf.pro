
% directed terms constructor
:-op(100,xfy,('=>')).

:-include('bbase.pro').

%% turns a term of the form H:-[B1,B2..] into binary =>/2 tree
fromBinTree(H,R):-(var(H),var(R)),!,R=H.
fromBinTree(H,R):-(atomic(H);atomic(R)),!,R=H.
fromBinTree((A=>B),(H:-Bs)):-fromBinTrees((A=>B),Bs,H).

fromBinTrees(H,[],R):-(var(H),var(R)),!,R=H.
fromBinTrees(H,[],R):-(atomic(H);atomic(R)),!,R=H.
fromBinTrees((A=>B),[HA|Bs],H):-fromBinTree(A,HA),fromBinTrees(B,Bs,H).

%% reverses from a =>/2 binary tree to the original term
toBinTree(A,B):-fromBinTree(B,A).

%% turns a term like f(a,b,...) into f:-[a,b,...]
listify(T,H):-var(T),!,H=T.
listify(T,H):-atomic(T),!,H=T.
listify(T,(F:-Ys)):-T=..[F|Xs],
  maplist(listify,Xs,Ys).

%% turns a term like   f:-[a,b,...] into f(a,b,...)
functorize(H,T):-var(H),!,T=H.
functorize(H,T):-atomic(H),!,T=H.
functorize((F:-Ys),T):-
  maplist(functorize,Ys,Xs),
  T=..[F|Xs].  
 
%%  form =/2 tree to term
toTerm-->fromBinTree,functorize.

%% from term to =/2 tree
fromTerm-->listify,toBinTree.


conj2list(A,[PA]):-var(A),!,to_pred(A,PA).
conj2list((A,B),[PA|Bs]):-!,lift_to_pred(A,PA),conj2list(B,Bs).
conj2list(A,[]):-A=true,!.
conj2list(A,[A]).

lift_to_pred(A,R):-var(A),!,to_pred(A,R).
lift_to_pred(A,A).


%% marks X as a user predicate p/1
to_pred(X,p(X)).

%% turns from  list into a conjunction
list2conj([],true).
list2conj([A|As],Cs):-list2conjs(A,As,Cs).

%list2conjs(p(A),[],R):-!,R=A.
list2conjs(A,[],A).
list2conjs(A,[B|Bs],(A,Cs)):-list2conjs(B,Bs,Cs).


%% binarized implicational normal form
to_bnf((H:-Bs),(HI:-BI) ):-
  to_bin((H:-Bs),(HC:-BC)),
  fromTerm(HC,HI),
  fromTerm(BC,BI).


%% binarization : a continuation passing form
to_bin((H:-Bs),(HC:-BC)):-
  add_continuation(H,C,HC),
  conj2list(Bs,Cs),
  bin_body(Cs,C,BC).
  
add_continuation(H,C,HC):-
  H=..[F|Xs],
  append(Xs,[C],Ys),
  HC=..[F|Ys].
  
bin_body([],C,C).
bin_body([B|Bs],C,BC):-
  bin_body(Bs,C,T),
  add_continuation(B,T,BC).

/*
% alternative binarization
% directly building arrow form
to_bc((H0:-Bs),(HC:-BC)):-
  fromTerm(H0,H),
  add_cont(H,C,HC),
  conj2list(Bs,Cs),
  bc_body(Cs,C,BC).

add_cont(C,A,A=>C).

bc_body([],C,C).
bc_body([B0|Bs],C,BC):-
  fromTerm(B0,B),
  bc_body(Bs,C,T),
  add_cont(B,T,BC).

*/

cls2bnf(Cls,BNF):-
  clausify(Cls,(H:-Bs)),
  to_bnf((H:-Bs),BNF).

% normalizes clauses to H:-B form
clausify((A:-B),R):-!,R=(A:-B).
clausify(A,(A:-true)).


%% returns clauses in file, one at a time
file2clause(F,C):-
  seeing(S),
  see(F),
  repeat,
    read(X),
    ( X=end_of_file,!,see(F),seen,see(S),fail
    ; C=X
    ).


basm:-
  InF='queens',
  OutF='out/bnf_asm.txt',
  basm(InF,OutF).

basm(InF):-
 OutF='out/bnf_asm.txt',
 basm(InF,OutF).

basm(InF,OutF):-
  atomic_list_concat(['progs/',InF,'.pro'],Source),
  to_basm(Source,OutF).


%% to "assembler"
to_basm(F,CF):-
  open(CF, write, Out),
  do((
    file2clause(F,C),
    cls2bnf(C,(H:-B)),
    ppp((H:-B)),
    to_postfix(H,PostFixsH),
    to_postfix(B,PostFixsB),
    append([PostFixsH,[(:-)|PostFixsB],['$']],PostFixs),
    numbervars(PostFixs,0,_),
    [First|Xs]=PostFixs,
    write(Out,First),
    do((
       member(X,Xs),
       write(Out,' '),
       write(Out,X)
    )),
    nl(Out)
  )),
  close(Out),
  nl.


to_postfix(Tree,Pfs):-to_postfix(Tree,Pfs,[]).

to_postfix(A)-->{var(A);atomic(A)},!,[A].
to_postfix(A=>B)-->to_postfix(A),to_postfix(B),['$'].



bin2paths(T,Pss):-
  bin2path(T,[],Pss,[]).
  %maplist(reverse,Pss,Rss).

bin2path(A,Ps)-->{var(A)},!,[A:Ps].
bin2path(A,Ps)-->{atomic(A)},!,[A:Ps].
bin2path((A=>B),Ps)-->
   bin2path(A,[0|Ps]),
   bin2path(B,[1|Ps]).


bin2pairs(T,Xs):-
  bin2paths(T,Pss),
  maplist(path2pair,Pss,Xs).

path2pair(K:Bs,K:X):-fromBBase(2,Bs,X).

term2pairs-->
  fromTerm,
  bin2paths.


term2pairs-->
  fromTerm,
  bin2pairs.

etest:-
  T=f(X,g(a,X,h(42,Y),c),Y),
  TT=f(xx,g(a,_XX,h(42,_YY),c),dd),
  ppp(T),nl,
  term2pairs(T,Pss),
  term2pairs(T,Xs),
  ppp(Pss),nl,
  ppp(Xs),nl,
  term2pairs(TT,XXs),
  Xs=XXs,
  ppp(T=TT),
  fail.

% helpers

c:-make.

:-op(800,fx,ppp).
:-op(1111,fx,do).

ppp(X):-portray_clause(X).

do(X):-X,fail;true.
