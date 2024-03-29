from collections import defaultdict
import json
import csv

from .unify import unifyToTerm, unifyWithEnv, \
    const_of
from .parser import parse
from .scanner import Int


def make_index():
    return defaultdict(set)


def add_clause(index, css, h):
    i = len(css)
    css.append(h)
    for c in const_of(h):
        index[c].add(i)


def tuplify(t):
    if isinstance(t, list):
        return tuple(map(tuplify, t))
    if isinstance(t, tuple):
        return tuple(map(tuplify, t))
    elif isinstance(t, int):
        return Int(t)
    else:
        return t


class Db:
    def __init__(self):
        self.index = make_index()  # content --> int index
        self.css = []  # content as ground tuples

    # parses text to list of ground tuples
    def digest(self, text):
        for cs in parse(text, ground=True):
            self.add_clause(cs)

    # loads from json list of lists
    def load_json(self, fname):
        with open(fname, 'r') as f:
            ts = json.load(f)
        for t in ts:
            self.add_db_clause(t)

    def load_csv(self, fname, delimiter=','):
        with open(fname) as f:
            wss = csv.reader(f, delimiter=delimiter)
            for ws in wss:
                self.add_db_clause(ws)

    def load_tsv(self, fname):
        self.load_csv(fname, delimiter='\t')

    def add_db_clause(self, t):
        self.add_clause(tuplify(t))

    # loads ground facts .nat or .json files
    def load(self, fname):
        if len(fname) > 4 and fname[-4:] == '.nat':
            with open(fname, 'r') as f:
                self.digest(f.read())
        elif len(fname) > 4 and fname[-4:] == '.tsv':
            self.load_tsv(fname)
        elif len(fname) > 4 and fname[-4:] == '.csv':
            self.load_csv(fname)
        else:
            self.load_json(fname)

    def save(self, fname):
        with open(fname, "w") as g:
            json.dump(self.css, g)

    # adds a clause and indexes it for all constants
    # recursively occurring in it, in any subtuple
    def add_clause(self, cs):
        add_clause(self.index, self.css, cs)

    def ground_match_of(self, query):
        """
        computes all ground matches of a query term in the Db;
        if a constant occurs in the query, it must also occur in
        a ground term that unifies with it, as the ground term
        has no variables that would match the constant
        """
        # find all constants in query
        constants = const_of(query)
        if not constants:
            # match against all clauses css, no help from indexing
            return set(range(len(self.css)))
        # pick a copy of the first set where c occurs
        first_constant = next(iter(constants))
        matches = self.index[first_constant].copy()
        # shrink it by intersecting with sets  where other constants occur
        for x in constants:
            matches &= self.index[x]
        # these are all possible ground matches - return them
        return matches

    # uses unification to match ground fact
    # with bindining applied to vs and colelcted on trail
    def unify_with_fact(self, h, vs, trail):
        ms = self.ground_match_of(h)
        for i in ms:
            h0 = self.css[i]
            u = unifyWithEnv(h, h0, vs, trail=trail, ocheck=False)
            yield u

    # uses unification to match and return ground fact
    def match_of(self, h):
        ms = self.ground_match_of(h)
        for i in ms:
            h0 = self.css[i]
            u = unifyToTerm(h, h0)
            if u: yield u

    # searches for a matching tuple
    def search(self, query):
        qss = parse(query, ground=False)
        for qs in qss:
            for rs in self.match_of(qs):
                yield rs

    # simple search based on content
    def about(self, query):
        qss = parse(query, ground=True)
        for qs in qss:
            qs = tuple(qs)
            for i in self.ground_match_of(qs):
                yield self.css[i]

    def ask_about(self, query):
        print('QUERY:', query)
        for r in self.about(query):
            print('-->', r)
        print('')

    # queries the Db directly with a text query
    def ask(self, query):
        print('QUERY:', query)
        for r in self.search(query):
            print('-->', r)
        print('')

    # builds possibly very large string representation
    # of the facts contained in the Db
    def __repr__(self):
        xs = [str(cs) + '\n' for cs in enumerate(self.css)]
        return "".join(xs)
