

import sys
import os

import pprint



PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )

if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

# print("PACKAGE_DIR:", PACKAGE_DIR)

sys.path.insert(0, PACKAGE_DIR)


# textblob uses nltk
import nltk

import pattern

import wn

import textblob

