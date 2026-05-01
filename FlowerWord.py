
"""The name Flowerword came from the first implementation inside the flowerewolf library. Just a collection of that missing 'en' functions.

The name stuck.
"""



import time
import io

kwdbg = 0
import pdb
import pprint
pp = pprint.pprint

# seed(1)

# need to import linguistics first - sets up sys.path and corpus/data folders for the sublibs
import linguistics

import pattern
import pattern.en

from pattern.en import article, referenced
from pattern.en import pluralize, singularize
from pattern.en import comparative, superlative
from pattern.en import conjugate, lemma, lexeme, tenses
from pattern.en import number, numerals, quantify, reflect, suggest, ngrams
from pattern.en import parse, tokenize, tag, parsetree, tree
from pattern.en import Sentence, Word, Chunk, PNPChunk, sentiment, mood, modality


from pattern.en import NOUN, VERB, ADJECTIVE, DEFINITE, INDEFINITE
from pattern.en import INDICATIVE, IMPERATIVE, CONDITIONAL, SUBJUNCTIVE
from pattern.en import SINGULAR, PLURAL

from pattern.text import IMPERFECTIVE, PERFECTIVE, PROGRESSIVE
from pattern.text import INFINITIVE, PRESENT, PAST, FUTURE

import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = en.wordnet


# synonym = a word that is similar in meaning,
# hypernym = a word with a broader meaning,       (tree => plant)
# hyponym = a word with a more specific meaning, (tree => oak)
# holonym = a word that is the whole of parts,   (tree => forest)
# meronym = a word that is a part of the whole,  (tree => trunk)
# antonym = a word that is opposite in meaning.

class FlowerWord:
    def __init__(self, word):
        # pdb.set_trace()
        self.word = word
        self.synset = None
        self.synsets = wordnet.synsets( word )
        self.idx = 0
        
        self.antonym = ""
        self.gloss = ""
        self.synonyms = []
        self.lexname = ""
        self.ic = 0.0
        
        
        if len(self.synsets) > 0:
            self.synset = self.synsets[0]
            self.synonyms = self.synset.synonyms
            self.antonym = self.synset.antonym
            self.gloss = self.synset.gloss
            self.lexname = self.synset.lexname
            self.ic = self.synset.ic

    def hyponyms(self):
        result = []
        for synset in self.synsets:
            hyponyms = synset.hyponyms()
            for hyponym in hyponyms:
                synonyms = hyponym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result

    def hypernyms(self):
        result = []
        for synset in self.synsets:
            hypernyms = synset.hypernyms()
            for hypernym in hypernyms:
                synonyms = hypernym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result


    def senses(self):
        result = []
        for synset in self.synsets:
            senses = synset.senses
            result.append( senses )
        return result


    def holonyms(self):
        result = []
        for synset in self.synsets:
            holonyms = synset.holonyms()
            for holonym in holonyms:
                synonyms = holonym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result


    def meronyms(self):
        result = []
        for synset in self.synsets:
            meronyms = synset.meronyms()
            for meronym in meronyms:
                synonyms = meronym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result


    def print(self):
        print("FlowerWord( %s )" % (self.word,))
        print("      synsets:", self.synsets )
        print("      antonym:", self.antonym )
        print("        gloss:", self.gloss )
        print("       synset:", self.synset )
        print("      lexname:", self.lexname )
        print("     hyponyms:", self.hyponyms() )
        print("    hypernyms:", self.hypernyms() )
        print("       senses:", self.senses() )
        print("     holonyms:", self.holonyms() )
        print("     meronyms:", self.meronyms() )


