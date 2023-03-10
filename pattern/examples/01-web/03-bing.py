from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))
import pattern

from pattern.web import Bing, Google, asynchronous, plaintext
from pattern.web import SEARCH, IMAGE, NEWS

import time

# This example retrieves results from Bing based on a given query.
# The Bing search engine can retrieve up to a 1000 results (10x100) for a query.

# Bing's "Custom Search API" is a paid service.
# The pattern.web module uses a test account by default,
# with 5000 free queries per month shared by all Pattern users.
# If this limit is exceeded, SearchEngineLimitError is raised.
# You should obtain your own license key at:
# https://datamarket.azure.com/account/
engine = Google(license=None, language="en")

# Quote a query to match it exactly:
q = "\"is more important than\""

# When you execute a query,
# the script will halt until all results are downloaded.
# In apps with an infinite main loop (e.g., GUI, game),
# it is often more useful if the app keeps on running
# while the search is executed in the background.
# This can be achieved with the asynchronous() function.
# It takes any function and that function's arguments and keyword arguments:
request = asynchronous(engine.search, q, start=1, count=100, type=SEARCH, timeout=10)

# This while-loop simulates an infinite application loop.
# In real-life you would have an app.update() or similar
# in which you can check request.done every now and then.
while not request.done:
    time.sleep(0.1)
    print(".", end="")

print("")
print("")

# An error occured in engine.search(), raise it.
if request.error:
    raise request.error

# Retrieve the list of search results.
for result in request.value:
    print(result.text)
    print(result.url)
    print("")
