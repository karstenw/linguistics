from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int
from builtins import range

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))
import pattern

from pattern.web import Bing, Google, plaintext
from pattern.en import parsetree
from pattern.search import Pattern
from pattern.db import Datasheet, pprint

# "X IS MORE IMPORTANT THAN Y"
# Here is a rough example of how to build a web miner.
# It mines comparative statements from Bing and stores the results in a table,
# which can be saved as a text file for further processing later on.

# Pattern matching also works with Sentence objects from the MBSP module.
# MBSP's parser is much more robust (but also slower).
#from MBSP import Sentence, parse

q = '"more important than"'          # search query
print("search query:", q )
p = "NP VP? more important than NP"  # Search pattern.
print("search pattern:", p )
p = Pattern.fromstring(p)
d = Datasheet()

resultcounter = 0
# engine = Bing(license=None)
engine = Google(license=None)
for i in range( 1 ):  # max=10
    for result in engine.search(q, start=i + 1, count=100, cached=True):
        s = result.description
        #print(result.url)
        #print(s)
        #print()
        s = plaintext(s)
        t = parsetree(s)
        for m in p.search(t):
            a = m.constituents(constraint=0)[-1] # Left NP.
            b = m.constituents(constraint=5)[0]  # Right NP.
            d.append((
                a.string.lower(),
                b.string.lower()))
            resultcounter += 1

print("Datasheet:")
pprint(d)

# print("resultcounter:", resultcounter)
print("")
print("%s results." % len(d))
