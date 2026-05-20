from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int

import sys
import os, time
import pdb
sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))

import pattern
from pattern.de import article, referenced, pluralize, singularize
from pattern.de import comparative, superlative, conjugate, lemma, lexeme, tenses
from pattern.de import NOUN, VERB, ADJECTIVE


# The en module has a range of tools for word inflection:
# guessing the indefinite article of a word (a/an?),
# pluralization and singularization, comparative and superlative adjectives, verb conjugation.

# INDEFINITE ARTICLE
# ------------------
# The article() function returns the indefinite article (a/an) for a given noun.
# The definitive article is always "the". The plural indefinite is "some".
print(article("bär") + " Bär")
print("")

# The referenced() function returns a string with article() prepended to the given word.
# The referenced() funtion is non-trivial, as demonstrated with the exception words below:
for word in ["Stunde", "Einzeiler", "Europäer", "Universität", "Eule", "genannt", "Jahr"]:
    print( word, 'referenced:', referenced(word))
print("")
pdb.set_trace()
# PLURALIZATION
# -------------
# The pluralize() function returns the plural form of a singular noun (or adjective).
# The algorithm is robust and handles about 98% of exceptions correctly:
for word in ["part-of-speech", "Kind", "Hund", "Wolf", "Bär", "Küchenmesser"]:
    print(word, "pluralized:", pluralize(word))
print( 'pluralize("Krake"):', pluralize("Krake"))
print( 'pluralize("Matrix"):', pluralize("Matrix"))
print( 'pluralize("Matrix"):', pluralize("Matrix"))
print( 'pluralize("mein", pos=ADJECTIVE):',
        pluralize("mein", pos=ADJECTIVE))
print("")

# SINGULARIZATION
# ---------------
# The singularize() function returns the singular form of a plural noun (or adjective).
# It is slightly less robust than the pluralize() function.
for word in ["part-of-speech", "Kind", "Hundes", "Wolf", "Bär", "Küchenmesser",
             "Oktopoden", "Matrizen", "Matrixe"]:
    print(word, "singularized:", singularize(word))
print( 'singularize("unser", pos=ADJECTIVE):', singularize("unser", pos=ADJECTIVE))
print("")

# COMPARATIVE & SUPERLATIVE ADJECTIVES
# ------------------------------------
# The comparative() and superlative() functions give the comparative/superlative form of an adjective.
# Words with three or more syllables are simply preceded by "more" or "most".
for word in ["freundlich", "groß", "schön", "verletzt", "wichtig", "Schlecht"]:
    print("%s => %s => %s" % (word, comparative(word), superlative(word)))
print("")

# VERB CONJUGATION
# ----------------
# The lexeme() function returns a list of all possible verb inflections.
# The lemma() function returns the base form (infinitive) of a verb.
print("lexeme: %s" % lexeme("sein"))
print("lemma: %s" % lemma("war"))
print("")

# The conjugate() function inflects a verb to another tense.
# You can supply:
# - tense : INFINITIVE, PRESENT, PAST,
# - person: 1, 2, 3 or None,
# - number: SINGULAR, PLURAL,
# - mood  : INDICATIVE, IMPERATIVE,
# - aspect: IMPERFECTIVE, PROGRESSIVE.
# The tense can also be given as an abbreviated alias, e.g.,
# inf, 1sg, 2sg, 3sg, pl, part, 1sgp, 2sgp, 3sgp, ppl, ppart.
from pattern.de import PRESENT, SINGULAR
print( 'conjugate("sein", tense=PRESENT, person=1, number=SINGULAR, negated=False):',
        conjugate("sein", tense=PRESENT, person=1, number=SINGULAR, negated=False))
print( 'conjugate("sein", tense="1sg", negated=False):',
        conjugate("sein", tense="1sg", negated=False))
print("")

# Prefer the full constants for code that will be reused/shared.

# The tenses() function returns a list of all tenses for the given verb form.
# Each tense is a tuple of (tense, person, number, mood, aspect).
# For example: tenses("are") => [('present', 2, 'plural', 'indicative', 'imperfective'), ...]
# You can then check if a tense constant is in the list.
# This will also work with aliases, even though they are not explicitly in the list.
from pattern.de import PRESENT, PLURAL
print( 'tenses("sind"):', tenses("sind"))
print('(PRESENT, 1, PLURAL) in tenses("sind"):',
       (PRESENT, 1, PLURAL) in tenses("sind"))
print("pl" in tenses("sind"))
