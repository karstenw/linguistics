<!-- $theme: default -->

# Linguistics

Several accumulated linguistics modules ([pattern](https://github.com/clips/pattern), [wn](https://github.com/goodmami/wn), [textblob](https://pypi.org/project/textblob/) & [nltk](https://www.nltk.org/) ) for Nodebox 1 to replace the "en" library.

Additionally there is the new conceptnetreader library which gives access to a local conceptnet database. 


These are the installed sources of the libraries. I am currently using Python 3.13.13 but this also worked with 3.11.4 and 3.8.12

# ATTENTION

## First Run

Rename the downloaded folder "linguistics" and place it inside the Nodebox "Library" folder.

Before the first run, open and run `DOWNLOAD_DATABASES_AND_INSTALL_CONCEPTNET.py` inside the linguistics folder. This downloads the needed corpora for `nltk`, `textblob`, `wn` and installs the conceptnet database. The data folder `linguistics-data` will be placed in the same folder as the `linguistics` folder. The runtime  is ca. 10 minutes.

#### nltk corpora for textblob, wn and pattern

If you run it from NodeBox there will be no feedback except the spinning beachball. 

Alternatively you can run it from the terminal with a current python3.



## General

This is a work in progress, a moving target.

Goals:

1. Make it available to Nodebox1

1. Keep it usable from a standard python3

1. Adapt Nodebox1 scripts using "en", "web"



### Usage

In a nodebox script do:

```python

import linguistics
```

After the linguistics import the submodules pattern, wn,nltk & textblob can be accessed with  `import pattern`, `import nltk`, `import wn`, `import textblob`.

