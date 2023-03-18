<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230317172542.2" a="E"><vh>linguistics</vh>
<v t="karstenw.20230317172648.1" a="E"><vh>@clean __init__.py</vh>
<v t="karstenw.20230317172648.2"><vh>Declarations</vh></v>
<v t="karstenw.20230317172648.3"><vh>nltk init</vh></v>
<v t="karstenw.20230317172648.4"><vh>textblob init</vh></v>
<v t="karstenw.20230317172812.1"><vh>wn init</vh></v>
<v t="karstenw.20230317172816.1"><vh>pattern init</vh></v>
<v t="karstenw.20230317172931.1"><vh>tools</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230317172542.2"></t>
<t tx="karstenw.20230317172648.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230317172648.2">import sys
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



</t>
<t tx="karstenw.20230317172648.3">from . import nltk
# from . import nltk.wordnet
wordnet = nltk.wordnet
nltk.data.path = [os.path.join( DATA_DIR, 'nltk-data' )]

# nltk.download( download_dir=nltk.data.path[0] )
#
# nltk.download( "wordnet_ic", download_dir=nltk.data.path[0] )
# nltk.download( "wordnet", download_dir=nltk.data.path[0] )



</t>
<t tx="karstenw.20230317172648.4"># TextBlob, Word, Sentence, Blobber, WordList
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

</t>
<t tx="karstenw.20230317172812.1">"""
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
    


</t>
<t tx="karstenw.20230317172816.1">from . import pattern
# change pattern webcache setting in pattern/web/cache/__init__.py



</t>
<t tx="karstenw.20230317172931.1">if 0:
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


</t>
</tnodes>
</leo_file>
