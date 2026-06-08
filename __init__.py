import sys
import os
import time

import pprint
pp = pprint.pprint

import pdb
kwlog = 1
kwdbg = 1



# directory init
#
# set data path "linguistics-data"
#
# insert current directory into sys.path

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

if kwlog:
    print("PACKAGE_DIR:", PACKAGE_DIR)

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

if kwlog:
    print("DATA_DIR:", DATA_DIR)

if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)


init_time = time.time()

import pattern

# no data path init - instead
# change pattern webcache setting in pattern/web/cache/__init__.py



nltk_time = time.time()
if kwlog:
    print("SYS import pattern: %.3f" % (nltk_time-init_time)  )

#
# NLTK
#
import nltk


# data path init
nltk.data.path = [os.path.join( DATA_DIR, 'nltk-data' )]

wn_time = time.time()
if kwlog:
    print("SYS import nltk: %.3f" % (wn_time-nltk_time)  )



"""
This is the wn interface for NodeBox and possibly others.

"""

import wn
    
# data path init
wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )

textblob_time = time.time()
if kwlog:
    print("SYS import wn: %.3f" % (textblob_time-wn_time)  )


# not sure what to use yet
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

import textblob

conceptnetreader_time = time.time()
if kwlog:
    print("SYS import textblob: %.3f" % (conceptnetreader_time-textblob_time)  )


import conceptnetreader

FlowerWord_time = time.time()
if kwlog:
    print("SYS import conceptnetreader: %.3f" % (FlowerWord_time-conceptnetreader_time)  )


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


import FlowerWord

end_time = time.time()

if kwlog:
    print("SYS import FlowerWord: %.3f" % (end_time - FlowerWord_time)  )
    print("SYS import linguistics: %.3f" % (end_time - init_time)  )

