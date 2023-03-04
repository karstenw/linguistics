from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int

import os
import sys
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
pattern = ximport("pattern")

from pattern.web import Newsfeed, plaintext, URL
from pattern.db import date

# This example reads a given RSS or Atom newsfeed channel.
# Some example feeds to try out:
NATURE = "http://feeds.nature.com/nature/rss/current"
# SCIENCE = "https://www.science.org/content/page/email-alerts-and-rss-feeds"
SCIENCE = "https://www.science.org/rss/news_current.xml"
NYT = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
TIME = "http://feeds.feedburner.com/time/topstories"
CNN = "http://rss.cnn.com/rss/edition.rss"
SCRIPTINGNEWS = "http://scripting.com/rss.xml"

engine = Newsfeed()

for result in engine.search(NATURE, cached=True):
    print(result.title.upper())
    print(plaintext(result.text))  # Remove HTML formatting.
    print(result.url)
    print(result.date)
    print("")

# News item URL's lead to the page with the full article.
# This page can have any kind of formatting.
# There is no default way to read it.
# But we could just download the source HTML and convert it to plain text:

#html = URL(result.url).download()
#print(plaintext(html))

# The resulting text may contain a lot of garbage.
# A better way is to use a DOM parser to select the HTML elements we want.
# This is demonstrated in one of the next examples.
