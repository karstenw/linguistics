from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..","..","..")))
import pattern

from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT

# The pattern.web module has a number of convenient search engines, as demonstrated.
# But often you will need to handle the HTML in web pages of your interest manually.
# The DOM object can be used for this, similar to the Javascript DOM.
# The DOM (Document Object Model) parses a string of HTML
# and returns a tree of nested Element objects.
# The DOM elements can then be searched by tag name, CSS id, CSS class, ...

# For example, top news entries on Reddit are coded as:
# <div class="_1poyrkZ7g36PawDueRza-J s1r3zmnv-7 bmeGah">
#     ...
#     <span class="y8HYJ-y_lTUHkQIc1mdCq yj3st6-1 kYJFRo">
#     ...
#         <a class="SQnoC3ObvgnGjWt90zD9Z " href="http://i.imgur.com/yDyPu8P.jpg">Bagel the bengal, destroyer of boxes</a>
#     ...
# </div>
#
# ... which - naturally - is a picture of a cat.
url = URL("https://www.reddit.com/top/")
dom = DOM(url.download(cached=True))
#print(dom.body.content)
for e in dom.by_tag("div._1poyrkZ7g36PawDueRza-J s1r3zmnv-7 bmeGah")[:5]: # Top 5 reddit entries.
    for a in e.by_tag("a.SQnoC3ObvgnGjWt90zD9Z")[:1]:
        print(plaintext(a.content))
        print(a.attrs["href"])
        print("")

# The links in the HTML source code may be relative,
# e.g., "../img.jpg" instead of "www.domain.com/img.jpg".
# We can get the absolute URL by prepending the base URL.
# However, this can get messy with anchors, trailing slashes and redirected URL's.
# A good way to get absolute URL's is to use the module's abs() function:
from pattern.web import abs
url = URL("https://nodebox.net")
for link in DOM(url.download()).by_tag("a"):
    link = link.attrs.get("href", "")
    link = abs(link, base=url.redirect or url.string)
    print(link)

# The DOM object is a tree of nested Element and Text objects.
# All objects inherit from Node (check the source code).

# Node.type       : NODE, TEXT, COMMENT, ELEMENT or DOM
# Node.parent     : Parent Node object.
# Node.children   : List of child Node objects.
# Node.next       : Next Node in Node.parent.children.
# Node.previous   : Previous Node in Node.parent.children.

# DOM.head        : Element with tag name "head".
# DOM.body        : Element with tag name "body".

# Element.tag     : Element tag name, e.g. "body".
# Element.attrs   : Dictionary of tag attributes, e.g. {"class": "header"}
# Element.content : Element HTML content as a string.
# Element.source  : Element tag + content

# Element.get_element_by_id(value)
# Element.get_elements_by_tagname(value)
# Element.get_elements_by_classname(value)
# Element.get_elements_by_attribute(name=value)

# You can also use shorter aliases (we prefer them):
# Element.by_id(), by_tag(), by_class(), by_attr().

# The tag name passed to Element.by_tag() can include
# a class (e.g., "div.message") or an id (e.g., "div#header").

# For example:
# In the <head> tag, retrieve the <meta name="keywords"> element.
# Get the string value of its "content" attribute and split into a list:
dom = DOM(URL("https://www.apple.com/uk/").download(cached=True))
kw = dom.head.by_attr(name="Description")[0]
kw = kw.attrs["content"]
print(kw)
print("")

# If you know CSS, you can also use short and handy CSS selectors:
# http://www.w3.org/TR/CSS2/selector.html
# Element(selector) will return a list of nested elements that match the given string.
#dom = DOM(URL("http://www.clips.ua.ac.be").download())
dom = DOM(URL("https://www.uantwerpen.be/en/research-groups/clips/").download())
for e in dom("div#ContentPlaceHolder1_ctl00_ctl01_Omkadering span div:contents p"):
    print(plaintext(e.content))
    print("")



######################################## Test Techcrunch - https://techcrunch.com/ ####################################

print("#"*40, "Test Techcrunch", "#"*40)
url = URL("https://techcrunch.com/category/startups/")
dom = DOM(url.download(cached=True))

for e in dom.by_tag("header.post-block__header")[:5]:
    for a in e.by_tag("h2.post-block__title")[:1]:
        print(plaintext(a.content))
        for h in a.by_tag("a.post-block__title__link")[:1]:
            print(h.attrs["href"])
        print("")
print("\n")

header = dom.by_class("river__title")[0]
print(header.content)
print("\n")


title_image = dom.by_attr(name="msapplication-TileImage")[0]
print(title_image.attrs['content'])
print("\n")


url = URL("https://techcrunch.com")
dom = DOM(url.download(cached=True))
for k in dom.by_class("post-block__title__link"):
    print(k.content.strip())
    print("")

print("\n")

for e in dom("header:post-block__header h2:post-block__title a:post-block__title__link"):
    print(e.content.strip())
    print(e.attrs["href"])
    print("")


################################ Test Habr - https://habr.com ####################################

print("#"*40, "Test Habr", "#"*40)
url = URL("https://habr.com/en/all/")
dom = DOM(url.download(cached=True))

for e in dom.by_tag("h2.post__title")[:5]:
    for a in e.by_tag("a.post__title_link")[:1]:
        print(plaintext(a.content))
        print("")
print("\n")

for k in dom.by_class("post__hubs inline-list"):
    for p in k.by_tag("li.inline-list__item inline-list__item_hub"):
        for t in p.by_tag("a.inline-list__item-link hub-link "):
            print(t.content)
print("\n")


descr = dom.by_attr(name="description")[0]
print(descr.attrs['content'])
print("\n")

for p in dom("div#broadcast_tabs_posts"):
    for e in p.by_class("content-list content-list_most-read"):
        for k in e.by_tag("a.post-info__title post-info__title_large"):
            print(plaintext(k.content))
        print("")