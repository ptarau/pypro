swipl -s bnf.pro -g "(basm('$1'),halt)"
time pypy3 bnf.py
