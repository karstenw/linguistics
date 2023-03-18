import sys
import os

import pprint
pp = pprint.pprint
import pdb



PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

# print("PACKAGE_DIR:", PACKAGE_DIR)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)



from . import nltk
# from . import nltk.wordnet
wordnet = nltk.wordnet
nltk.data.path = [os.path.join( DATA_DIR, 'nltk-data' )]

# nltk.download( download_dir=nltk.data.path[0] )
#
# nltk.download( "wordnet_ic", download_dir=nltk.data.path[0] )
# nltk.download( "wordnet", download_dir=nltk.data.path[0] )



# TextBlob, Word, Sentence, Blobber, WordList
from . import textblob

# from . textblob import *
# import textblob.Word


# textblob downloads via nltk
#
# minimal
# brown, punkt, wordnet, averaged_perceptron_tagger
#
# all
# + conll2000, movie_reviews


# pattern nltk downloads
# 
# wordnet_ic

"""
This is the wn interface for NodeBox and possibly others.

"""

from . import wn

wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )

# wn.download("omw")
# wn.download("odenet")
# wn.download("oewn")
# wn.download("cili")


# not suere what to use yet
if 0:
    # check if english lexicon is loaded
    try:
        prj = wn.config.get_project_info("oewn")
    except TypeError as err:
        print( err )
    
    en = wn.wordnet("oewn")

    lexicons = {}
    for lexicon in wn.lexicons():
        lang = lexicon.language
        lid = lexicon.id
        label = lexicon.label
        if lang not in lexicons:
            lexicons[lang] = []
        lexicons[lang].append( (lang, lid, label, lexicon) )
    


from . import pattern
# change pattern webcache setting in pattern/web/cache/__init__.py



if 0:
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


