## A lightweight Prolog-like interpeter with a natural-language style syntax 

* Terms are represented as nested tuples.

* A parser and scanner for a simplified Prolog term syntax is used
to turn terms into nested Python tuples.

Surface syntax of facts, as read from strings, is just whitespace separated words 
(with tuples paranthesized) and
sentences ended with ```.``` or ```?```.
Like in Prolog, variables are capitalized, unless quoted. Example programs are in folder ```natprogs```, for instance ```tc.nat```:

```
cat is feline.
tiger is feline.
mouse is rodent.
feline is mammal.
rodent is mammal.
snake is reptile.
mammal is animal.
reptile is animal.

tc A Rel B : A Rel B.
tc A Rel C : A Rel B, tc B Rel C.
```

To query it, try:

``` python3 -i natlog.py

>>> n=natlog(file_name="natprogs/tc.nat")
>>> n.query("tc Who is What ?")
```

It will return the transitive closure of the ```is``` relation.

List processing is also supported as in:

```
app () Ys Ys. 
app (X Xs) Ys (X Zs) : app Xs Ys Zs.
```
## A nested tuple store for unification-based tuple mining

* An indexer in combination with the unification algorithm is used
to retrieve ground terms matching terms containing logic variables.

Indexing is on all constants occurring in 
ground facts placed in a database. 

As facts are ground,
unification has occurs check and trailing turned off when searching
for a match.

To try it out, do:

```python3 -i db.py```

`````>>> dbtest()`````

It gives, after digesting a text and then querying it:

```
   John has (a car).
   Mary has (a bike).
   Mary is (a student).
   John is (a pilot).
   
('John', 'has', ('a', 'car'))
('Mary', 'has', ('a', 'bike'))
('Mary', 'is', ('a', 'student'))
('John', 'is', ('a', 'pilot'))


Who has (a What)?
--> ('John', 'has', ('a', 'car'))
--> ('Mary', 'has', ('a', 'bike'))

Who is (a pilot)?
--> ('John', 'is', ('a', 'pilot'))

'Mary' is What?
--> ('Mary', 'is', ('a', 'student'))

'John' is (a What)?
--> ('John', 'is', ('a', 'pilot'))

Who is What?
--> ('Mary', 'is', ('a', 'student'))
--> ('John', 'is', ('a', 'pilot'))

```
