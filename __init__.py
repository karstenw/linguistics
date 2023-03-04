

import sys
import os

import pprint
pp = pprint.pprint
import pdb
#pdb.set_trace()

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PACKAGE_DIR)

from . import nltk

# TextBlob, Word, Sentence, Blobber, WordList
from . import textblob
# from . textblob import *
# import textblob.Word

from . import wn

from . import pattern


from . import en



# from . import nltk.wordnet
wordnet = nltk.wordnet

# nltk.download( download_dir=nltk.data.path[0] )



def _firstwordtags( wl ):
    tb = TextBlob( wl )
    if not tb:
        return ""
    for word,tag in tb.tags:
        return word,tag


def is_noun( w ):
    _,tag = _firstwordtags( w )
    if tag in ('NN','NNP'):
        return True
    return False


def is_verb( v ):
    _,tag = _firstwordtags( w )
    return wordnet.is_verb( v )

def is_adjective( a ):
    _,tag = _firstwordtags( w )
    return wordnet.is_adjective( a )

def is_adverb( a ):
    _,tag = _firstwordtags( w )
    return wordnet.is_adverb( a )


