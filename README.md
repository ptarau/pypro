## A nested tuple store for unification-based tuple mining.

* Terms are represented as nested tuples.

* A parser and scanner for a simplified Prolog term syntax is used
to turn terms into nested Python tuples.

* An indexer in combination with the unification algorithm is used
to retrieve ground terms matching terms containing logic variables.

Surface syntax of facts, as read from strings, is just whitespace separated words 
(with tuples paranthesized) and
sentences ended with ```.``` or ```?```.
Like in Prolog, variables are capitalized, unless quoted.

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
