
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
import pattern.text
import pattern.text.en
en = pattern.text.en
wordnet = en.wordnet

class FlowerWord:
    def __init__(self, word):
        # pdb.set_trace()
        self.word = word
        self.synsets = wordnet.synsets( word )
        self.idx = 0
        self.antonym = ""
        self.gloss = ""
        self.synset = None
        self.synonyms = []
        self.antonym = ""
        self.gloss = ""
        self.lexname = ""

        if len(self.synsets) > 0:
            synonyms = self.synsets[0].synonyms
            try:
                self.idx = synonyms.index(word)
                w = self.synset = self.synsets[self.idx]
                #print("Found synset:", w)
            except:
                w = self.synsets[0]
                #print("Use synset:", w)

            self.antonym = w.antonym
            self.gloss = w.gloss
            self.lexname = w.lexname

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
                synonyms = hyponym.synonyms
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
                synonyms = hyponym.synonyms
                for synonym in synonyms:
                    synonym = synonym.replace("_", " ")
                    result.append( synonym )
        result = list(set(result))
        return result



