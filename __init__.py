

import sys
import os

import pprint
pp = pprint.pprint
import pdb
#pdb.set_trace()

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# print("PACKAGE_DIR:", PACKAGE_DIR)
sys.path.insert(0, PACKAGE_DIR)



from . import nltk
# from . import nltk.wordnet
wordnet = nltk.wordnet




# TextBlob, Word, Sentence, Blobber, WordList
from . import textblob

# from . textblob import *
# import textblob.Word



from . import wn
wn.config.data_directory = os.path.join( PACKAGE_DIR, './wn-data' )
# wn.download("omw")
# wn.download("odenet")
# wn.download("cili")





from . import pattern



# for historical purposes only - halfway & errornesously py converted
from . import en



# nltk.download( download_dir=nltk.data.path[0] )
#
# nltk.download( "wordnet_ic", download_dir=nltk.data.path[0] )
# nltk.download( "wordnet", download_dir=nltk.data.path[0] )
#
#
# textblob downloads
#
# minimal
# brown, punkt, wordnet, averaged_perceptron_tagger
#
# all
# + conll2000, movie_reviews


# pattern nltk downloads
# 
# wordnet_ic


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


