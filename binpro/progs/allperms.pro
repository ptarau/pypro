goal(done):-all_permutations([1,2,3,4,5,6,7,8,9],_Ps).

all_permutations([],[[]]).
all_permutations([X|Xs],Perms2):-
       	all_permutations(Xs,Perms1),
        extend_permutations(Perms1,X,Perms2).

extend_permutations([],_,[]).
extend_permutations([Perm|Perms1],X,[[X|Perm]|Perms3]):-
	extend_permutations(Perms1,X,Perms2),
	insert_item(Perm,X,[],Perms2,Perms3).

insert_item([],_,_,Perms,Perms).
insert_item([Y|Ys],X,Acc,Perms1,[Zs|Perms2]):-
       	reverse_and_append(Acc,[Y,X|Ys],Zs),
        insert_item(Ys,X,[Y|Acc],Perms1,Perms2).

reverse_and_append([],Acc,Acc).
reverse_and_append([X|Xs],Acc,Zs):-
       reverse_and_append(Xs,[X|Acc],Zs).

       

