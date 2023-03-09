<!-- $theme: default -->

# Linguistics

Several accumulated linguistics modules ([pattern](https://github.com/clips/pattern), [wn](https://github.com/goodmami/wn), [textblob](https://pypi.org/project/textblob/) & [nltk](https://www.nltk.org/) ) for Nodebox 1 to replace the "en" library.


## First Run

Rename the downloaded folder "linguistics" and place it inside the "Library" folder.

Before the first run, open and run `download_corpora.py` inside the linguistics folder. This downloads the needed corpora to run. The data folder `linguistics-data` will be placed in the same folder as the `linguistics` folder.


## General

This is a work in progress, a moving target.


1. Make it available to Nodebox1

1. Keep it usable from a standard python3

1. Adapt Nodebox1 scripts using "en"



### Usage

In a nodebox script do:

```python

import linguistics
```

After the linguistics import the submodules pattern, wn,nltk & textblob can be accessed with `linguistics.nltk` or `import nltk`.

