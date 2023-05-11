import sys
import os
import time

import pprint
pp = pprint.pprint
import pdb

t1 = time.time()

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

# print("PACKAGE_DIR:", PACKAGE_DIR)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)



t2 = time.time()

if 1:
    import pattern

# no data path init - instead
# change pattern webcache setting in pattern/web/cache/__init__.py

t3 = time.time()
print("import pattern: %.3f" % (t3-t2)  )

# make a function
if 1:
    import nltk
    # wordnet = nltk.wordnet
    
    # data path init
    nltk.data.path = [os.path.join( DATA_DIR, 'nltk-data' )]

t4 = time.time()
print("import nltk: %.3f" % (t4-t3)  )



# nltk.download( download_dir=nltk.data.path[0] )
#
# nltk.download( "wordnet_ic", download_dir=nltk.data.path[0] )
# nltk.download( "wordnet", download_dir=nltk.data.path[0] )

# seems interesting
# nltk.download( "framenet_v17", download_dir=nltk.data.path[0] )



"""
This is the wn interface for NodeBox and possibly others.

"""

if 1:
    import wn
    
    # data path init
    wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )

def init_wn():
    import wn
    wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )
# wn.download("omw")
# wn.download("odenet")
# wn.download("oewn")
# wn.download("cili")
t5 = time.time()
print("import wn: %.3f" % (t5-t4)  )


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
    


# perhaps delete ? havent used this

# TextBlob, Word, Sentence, Blobber, WordList
if 1:
    import textblob

t6 = time.time()
print("import textblob: %.3f" % (t6-t5)  )

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

# conceptnet
# from . import conceptnetreader
# package path should be valid by now
import conceptnetreader

t7 = time.time()
print("import conceptnetreader: %.3f" % (t7-t6)  )

# data path init
conceptnetreader.databasefile = os.path.join( DATA_DIR, 'conceptnet-data', 'conceptnet.sqlite3' )
conceptnetreader.initlib()

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


