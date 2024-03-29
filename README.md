<!-- $theme: default -->

# Linguistics

Several accumulated linguistics modules ([pattern](https://github.com/clips/pattern), [wn](https://github.com/goodmami/wn), [textblob](https://pypi.org/project/textblob/) & [nltk](https://www.nltk.org/) ) for Nodebox 1 to replace the "en" library.

Additionally there is the new conceptnetreader library which gives access to a local conceptnet database.


These are the installed sources of the libraries. I am currently using Python 3.11.4 but this also worked with 3.8.12

# ATTENTION

## First Run

Rename the downloaded folder "linguistics" and place it inside the Nodebox "Library" folder.

Before the first run, open and run `download_corpora.py` inside the linguistics folder. This downloads the needed corpora for `nltk`, `textblob` and `wn` to run. The data folder `linguistics-data` will be placed in the same folder as the `linguistics` folder.


#### nltk corpora for textblob, wn and pattern

The runtime for `download_corpora.py` is ca. 20 minutes.

If you run it from NodeBox there will be no feedback except the spinning beachball. 

Alternatively you can run it from the terminal with a 3.8 or 3.11 python. Perhaps you must install the requirements first.

#### conceptnet database

For the conceptnet database open and run `install-conceptnet-database.py`.

The runtime for `install-conceptnet-database.py` is ca. 10 minutes.

As with the nltk download there is no feedback but it can be run from the terminal to see what's going on.


## General

This is a work in progress, a moving target.

Goals:

1. Make it available to Nodebox1

1. Keep it usable from a standard python3

1. Adapt Nodebox1 scripts using "en"



### Usage

In a nodebox script do:

```python

import linguistics
```

After the linguistics import the submodules pattern, wn,nltk & textblob can be accessed with `linguistics.nltk` or `import nltk`.

