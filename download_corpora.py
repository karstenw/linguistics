

import sys
import os
# import pdb
import pprint
import time

# pdb.set_trace()

start = time.time()

try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

print("PACKAGE_DIR:", PACKAGE_DIR)
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )

if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

# print("PACKAGE_DIR:", PACKAGE_DIR)

sys.path.insert(0, PACKAGE_DIR)


# textblob uses nltk
import nltk
nltk_data_dir = os.path.join( DATA_DIR, 'nltk-data' )
nltk.data.path = [ nltk_data_dir ]

nltk.download( "wordnet_ic", download_dir=nltk_data_dir )
nltk.download( "wordnet", download_dir=nltk_data_dir )
nltk.download( "sentiwordnet", download_dir=nltk_data_dir )

# textblob downloads
nltk.download( "brown", download_dir=nltk_data_dir )
nltk.download( "punkt", download_dir=nltk_data_dir )
nltk.download( "averaged_perceptron_tagger", download_dir=nltk_data_dir )
nltk.download( "conll2000", download_dir=nltk_data_dir )
nltk.download( "movie_reviews", download_dir=nltk_data_dir )


import wn
wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )
wn.download("omw")
wn.download("odenet")
wn.download("cili")

stop = time.time()
print("nltk & wn in %.3fsec" % (stop-start,) )
