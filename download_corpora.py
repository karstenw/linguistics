

import sys
import os

import pdb
kwdbg = True


import pprint
import time

start = time.time()

nb=True
try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    nb=False
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

if kwdbg:
    print("PACKAGE_DIR:", PACKAGE_DIR)

PARENT_DIR, _ = os.path.split( PACKAGE_DIR )
DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )

if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

sys.path.insert(0, PACKAGE_DIR)

# pdb.set_trace()

# if run from Nodebox do not accumulate endless messages...
# therefore 
#       quiet=nb
# or
#       progress_handler=pg

# textblob uses nltk
if 1:
    import nltk
    nltk_data_dir = os.path.join( DATA_DIR, 'nltk-data' )
    nltk.data.path = [ nltk_data_dir ]

    nltk.download( "wordnet", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet_ic", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "sentiwordnet", download_dir=nltk_data_dir, quiet=nb )

    nltk.download( "wordnet2021", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet2022", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet31", download_dir=nltk_data_dir, quiet=nb )


    # textblob minimal downloads
    # wordnet already loaded
    nltk.download( "brown", download_dir=nltk_data_dir, quiet=nb )
    #nltk.download( "punkt", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "punkt_tab", download_dir=nltk_data_dir, quiet=nb )
    #nltk.download( "averaged_perceptron_tagger", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "averaged_perceptron_tagger_eng", download_dir=nltk_data_dir, quiet=nb )

    # textblob additional
    nltk.download( "conll2000", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "movie_reviews", download_dir=nltk_data_dir, quiet=nb )


import wn
from wn.util import ProgressHandler, ProgressBar

pg = ProgressBar
if nb:
    pg = ProgressHandler
wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )

# https://github.com/omwn - open multilingual wordnet
wn.download("omw", add=True, progress_handler=pg)

# https://github.com/hdaSprachtechnologie/odenet - open german wordnet
wn.download("odenet", add=True, progress_handler=pg)

# https://github.com/globalwordnet/cili/ - collaborative interlingual index
wn.download("cili", add=True, progress_handler=pg)

stop = time.time()
print("nltk & wn in %.3fsec" % (stop-start,) )
