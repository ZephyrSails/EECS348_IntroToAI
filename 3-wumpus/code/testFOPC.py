import FOPC

# Please don't use this file to score us, our code is in wumpusHunter.py
# please use following command in HW directory to test the homework:

# python wumpusHunter.py

#

statement1 = ('clean', 'Cell 11')
statement2 = ('clean', 'Cell 12')
pattern = ('clean', '?x')
bindings = {}

first = FOPC.match(statement1,pattern,bindings)
print first

second = FOPC.match(statement2,pattern,first)
print second

print FOPC.instantiate(statement1, first)
