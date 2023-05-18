
import sys, os, pdb
sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))
import pattern
from pattern.web import Twitter
from pattern.en import Sentence, parse
from pattern.search import search
from pattern.vector import Document, Corpus, KNN
corpus = Corpus()
pdb.set_trace()
for i in range(1,15):
    for tweet in Twitter().search('#win OR #fail', start=i, count=100):
        p = '#win' in tweet.description.lower() and 'WIN' or 'FAIL'
        s = tweet.description.lower()
        s = Sentence(parse(s))
        s = search('JJ', s) # JJ = adjective s = [match[0].string for match in s]
        s = ' '.join(s)
        if len(s) > 0:
            corpus.append(Document(s, type=p))
classifier = KNN()
for document in corpus:
    classifier.train(document)
print( classifier.classify('sweet') )   # yields 'WIN'
print( classifier.classify('stupid') )  # yields 'FAIL'd
