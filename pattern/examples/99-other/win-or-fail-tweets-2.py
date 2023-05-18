import sys, os, pdb
sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))
import time

import pattern
from pattern.web import Twitter
from pattern.en import tag
from pattern.vector import KNN, count

twitter, knn = Twitter(), KNN()

pdb.set_trace()

for i in range(1, 2):
    j = 0
    for tweet in twitter.search('#win OR #fail', start=i, count=100):
        j += 1
        
        s = tweet.text.lower()
        p = '#win' in s and 'WIN' or 'FAIL'
        v = tag(s)
        v = [word for word, pos in v if pos == 'JJ'] # JJ = adjective
        
        print("\n\n\n")
        print("-" * 80)
        print( (i-1) * 100 + j )
        print(s)
        print("#####")
        print(v)
        print()
        v = count(v) # {'sweet': 1}
        if v:
            knn.train(v, type=p)

print(knn.classify('sweet potato burger'))
print(knn.classify('stupid autocorrect'))
