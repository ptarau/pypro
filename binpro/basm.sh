rm -f out/bnf_asm.*
swipl -s bnf.pro -g "basm('$1','out/bnf_asm.txt'),halt"
time python3 -O bnf.py
