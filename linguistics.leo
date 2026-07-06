<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="karstenw.20230317172542.2" a="E"><vh>linguistics</vh>
<v t="karstenw.20230317172648.1" a="E"><vh>@clean __init__.py</vh>
<v t="karstenw.20230317172648.2"><vh>Declarations</vh></v>
<v t="karstenw.20260606163217.1"><vh>Globals</vh></v>
<v t="karstenw.20230317172816.1"><vh>pattern init</vh></v>
<v t="karstenw.20230317172648.3"><vh>nltk init</vh></v>
<v t="karstenw.20230317172812.1"><vh>wn init</vh></v>
<v t="karstenw.20230317172648.4"><vh>textblob init</vh></v>
<v t="karstenw.20230428163032.1"><vh>conceptnet init</vh></v>
<v t="karstenw.20260628144829.1"><vh>Flowerword init</vh></v>
<v t="karstenw.20230317172931.1"><vh>tools</vh></v>
</v>
<v t="karstenw.20230524124241.1"><vh>@clean FlowerWord.py</vh>
<v t="karstenw.20230524124307.1"><vh>Declarations</vh></v>
<v t="karstenw.20260606163051.1"><vh>handleResult - TODO</vh></v>
<v t="karstenw.20230524124417.1"><vh>FlowerWord</vh>
<v t="karstenw.20230524124417.2"><vh>__init__</vh></v>
<v t="karstenw.20230524124417.3"><vh>hyponyms</vh></v>
<v t="karstenw.20230524124417.4"><vh>hypernyms</vh></v>
<v t="karstenw.20230524124417.5"><vh>senses</vh></v>
<v t="karstenw.20230524124417.6"><vh>holonyms</vh></v>
<v t="karstenw.20230524124417.7"><vh>meronyms</vh></v>
<v t="karstenw.20260501093741.1"><vh>print</vh></v>
</v>
</v>
<v t="karstenw.20230518135525.1"><vh>@clean download_corpora.py</vh>
<v t="karstenw.20230518135556.1"><vh>Declarations</vh></v>
<v t="karstenw.20260606162533.1"><vh>script</vh></v>
</v>
<v t="karstenw.20230521225929.1"><vh>@clean install-conceptnet-database.py</vh>
<v t="karstenw.20230521225929.2"><vh>Declarations 1</vh></v>
<v t="karstenw.20230521225929.3"><vh>Globals</vh></v>
<v t="karstenw.20230521225929.5"><vh>handleDataArchive</vh></v>
<v t="karstenw.20230521225929.6"><vh>readstatic</vh></v>
<v t="karstenw.20230521225929.7"><vh>importConceptnetTables</vh></v>
<v t="karstenw.20230521225929.8"><vh>sdb</vh>
<v t="karstenw.20260222150150.1"><vh>py3</vh></v>
<v t="karstenw.20260222150155.1"><vh>makeunicode</vh></v>
<v t="karstenw.20260222150200.1"><vh>datestring</vh></v>
<v t="karstenw.20230521225929.9"><vh>dotprinter</vh></v>
<v t="karstenw.20230521225929.10"><vh>tabline2items</vh></v>
<v t="karstenw.20230521225929.11"><vh>getconnection</vh></v>
<v t="karstenw.20230521225929.12"><vh>commit</vh></v>
<v t="karstenw.20230521225929.13"><vh>dict_factory</vh></v>
<v t="karstenw.20230521225929.14"><vh>getTableFieldnames</vh></v>
<v t="karstenw.20230521225929.15"><vh>createStatement</vh></v>
<v t="karstenw.20230521225929.16"><vh>createRecord</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230317172542.2"></t>
<t tx="karstenw.20230317172648.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230317172648.2">import sys
import os
import time

import pprint
pp = pprint.pprint

import pdb
kwlog = 1
kwdbg = 0



</t>
<t tx="karstenw.20230317172648.3">#
# NLTK
#
if 1: # need data.path init - fullinit:
    import nltk
    
    
    # data path init
    nltk.data.path = [os.path.join( DATA_DIR, 'nltk-data' )]
    
    wn_time = time.time()
    if kwlog:
        print("SYS import nltk: %.3f" % (wn_time-nltk_time)  )



</t>
<t tx="karstenw.20230317172648.4"># perhaps delete ? havent used this
# TextBlob, Word, Sentence, Blobber, WordList

if fullinit:
    import textblob
    
    conceptnetreader_time = time.time()
    if kwlog:
        print("SYS import textblob: %.3f" % (conceptnetreader_time-textblob_time)  )


</t>
<t tx="karstenw.20230317172812.1">"""
This is the wn interface for NodeBox and possibly others.

"""

if fullinit:
    import wn
        
    # data path init
    wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )
    
    textblob_time = time.time()
    if kwlog:
        print("SYS import wn: %.3f" % (textblob_time-wn_time)  )
    
    
    # not sure what to use yet
    if 0:
        # check if english lexicon is loaded
        try:
            prj = wn.config.get_project_info("oewn")
        except TypeError as err:
            print( err )
        
        en = wn.wordnet("oewn")
    
        lexicons = {}
        for lexicon in wn.lexicons():
            lang = lexicon.language
            lid = lexicon.id
            label = lexicon.label
            if lang not in lexicons:
                lexicons[lang] = []
            lexicons[lang].append( (lang, lid, label, lexicon) )


</t>
<t tx="karstenw.20230317172816.1">if fullinit:

    init_time = time.time()
    
    import pattern
    
    # no data path init - instead
    # change pattern webcache setting in pattern/web/cache/__init__.py
    
nltk_time = time.time()
if fullinit:
    if kwlog:
        print("SYS import pattern: %.3f" % (nltk_time-init_time)  )

</t>
<t tx="karstenw.20230317172931.1">if 0:
    def _firstwordtags( wl ):
        tb = TextBlob( wl )
        if not tb:
            return ""
        for word,tag in tb.tags:
            return word,tag
    
    
    def is_noun( w ):
        _,tag = _firstwordtags( w )
        if tag in ('NN','NNP'):
            return True
        return False
    
    
    def is_verb( v ):
        _,tag = _firstwordtags( w )
        return wordnet.is_verb( v )
    
    def is_adjective( a ):
        _,tag = _firstwordtags( w )
        return wordnet.is_adjective( a )
    
    def is_adverb( a ):
        _,tag = _firstwordtags( w )
        return wordnet.is_adverb( a )


</t>
<t tx="karstenw.20230428163032.1">if fullinit:
    import conceptnetreader
    
    FlowerWord_time = time.time()
    if kwlog:
        print("SYS import conceptnetreader: %.3f" % (FlowerWord_time-conceptnetreader_time)  )


</t>
<t tx="karstenw.20230518135525.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230518135556.1">

import sys
import os

import pdb
kwdbg = True


import pprint
import time

</t>
<t tx="karstenw.20230521225929.1">@language python
@tabwidth -4
@others
if 1: # __name__ == '__main__':
    print()
    # pdb.set_trace()
    handleDataArchive( sqlitezifile, basefolder )
    print()
    importConceptnetTables( importfiles )


</t>
<t tx="karstenw.20230521225929.10">def tabline2items( line ):
    line = line.strip(" \r\n")
    line = makeunicode( line )
    items = line.split( "\t" )
    return items


</t>
<t tx="karstenw.20230521225929.11">def getconnection( filepath ):
    """open sqlite db at filepath.

    returns either:
        connection to database OR
        0: parent folder does not exists. Something is wrong.
    """

    filepath = os.path.abspath( filepath )
    folder, filename = os.path.split( filepath )
    if not os.path.exists( folder ):
        return 0
    
    conn = sqlite3.connect( filepath,
                            detect_types=  sqlite3.PARSE_DECLTYPES
                                         | sqlite3.PARSE_COLNAMES)

    cursor = conn.cursor()
    cursor.execute("PRAGMA automatic_index=1;")

    return conn


</t>
<t tx="karstenw.20230521225929.12">def commit( conn ):
    ok = False
    i = 0
    while not ok:
        if i &gt; 20:
            break
        try:
            conn.commit()
            ok = True
        except sqlite3.OperationalError as err:
            debugprint("")
            debugprint( "ERR: " + repr(err) )
            time.sleep( 0.01 )
            i += 1


</t>
<t tx="karstenw.20230521225929.13">def dict_factory(cursor, row):
    # from pysqlite code examples
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


</t>
<t tx="karstenw.20230521225929.14">def getTableFieldnames(conn, tablename):

    oldfactory = conn.row_factory
    conn.row_factory = dict_factory

    c = conn.cursor()
    q = "PRAGMA table_info(%s);" % tablename
    c.execute(q)

    # extract fieldname from description
    fieldnames = []
    for rec in c:
        fieldnames.append( rec['name' ] )

    c.close()
    conn.row_factory = oldfactory
    return fieldnames


</t>
<t tx="karstenw.20230521225929.15">def createStatement( tablename, fieldnames ):
    """
    Create SELECT, INSERT and UPDATE statements from tablename and
    fieldname list.
    """
    u = "UPDATE %s SET " % (tablename,)
    nkeys = len(fieldnames)

    lfieldnames = ",".join(fieldnames)
    ifieldnames = '(' + lfieldnames + ')'
    qfieldnames = lfieldnames

    repmarks = [ '?'] * nkeys
    repmarks = ','.join( repmarks )

    q = "SELECT (%s) FROM %s" % ( lfieldnames, tablename )
    if nkeys &gt; 1:
        q = "SELECT %s FROM %s" % ( lfieldnames, tablename )
    
    i = "INSERT INTO %s (%s) VALUES (%s)" % ( tablename, lfieldnames, repmarks)
    
    ufielditems = []
    s = "%s=?"
    for f in fieldnames:
        ufielditems.append( s % f )
    ufieldnames = ",".join( ufielditems )
    u = u + ufieldnames

    result = []
    return (q,i,u)


</t>
<t tx="karstenw.20230521225929.16">def createRecord( conn, tablename, recordDict, docommit=True):

    fieldnames = []
    fieldvalues = []

    tablefieldnames = getTableFieldnames(conn, tablename)

    for item in recordDict.items():
        k,v= item
        if k in tablefieldnames:
            fieldnames.append( k )
            fieldvalues.append( v )

    q,i,u = createStatement( tablename, fieldnames )
    c = conn.cursor()

    if not fieldnames:
        i = "INSERT INTO `%s` DEFAULT VALUES;" % tablename
        c.execute( i )
    else:
        c.execute( i, fieldvalues )
    last = c.lastrowid
    if docommit:
        commit( conn )
    return last


</t>
<t tx="karstenw.20230521225929.2">

import sys
import os
import io
import time

import sqlite3
import unicodedata

import zipfile
import gzip

import pdb
import pprint
pp=pprint.pprint

nb = True
try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    nb = False
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

print("PACKAGE_DIR:", PACKAGE_DIR)

PARENT_DIR, _ = os.path.split( PACKAGE_DIR )
print("PARENT_DIR:", PARENT_DIR)
sys.path.insert(0, PARENT_DIR)


</t>
<t tx="karstenw.20230521225929.3">
DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )


ZIPFOLDER = os.path.join( PACKAGE_DIR, "conceptnetreader/data" )
sqlitezifile =  os.path.join( ZIPFOLDER, "conceptnet.sqlite3.zip" )
conceptsdump1 = os.path.join( ZIPFOLDER, "concept_aa.tab.gz" )
conceptsdump2 = os.path.join( ZIPFOLDER, "concept_ab.tab.gz" )
edgesdump1 = os.path.join( ZIPFOLDER, "edge_aa.tab.gz" )
edgesdump2 = os.path.join( ZIPFOLDER, "edge_ab.tab.gz" )
edgesdump3 = os.path.join( ZIPFOLDER, "edge_ac.tab.gz" )
edgesdump4 = os.path.join( ZIPFOLDER, "edge_ad.tab.gz" )

importfiles = (conceptsdump1, conceptsdump2,
               edgesdump1, edgesdump2, edgesdump3, edgesdump4 )

basefolder = os.path.join( DATA_DIR, "conceptnet-data" )
if not os.path.exists( basefolder ):
    os.makedirs( basefolder )

databasefile =  os.path.join( basefolder, "conceptnet.sqlite3" )
if 0:
    print("conceptsdump1:", conceptsdump1 )
    print("conceptsdump2:", conceptsdump2 )
    print("edgesdump1:", edgesdump1 )
    print("edgesdump2:", edgesdump2 )
    print("edgesdump3:", edgesdump3 )
    print("importfiles:", importfiles )
    print("databasefile:", databasefile )


exportfoldersqlite = os.path.join( basefolder, "sqliteimport")
exportfolderfilemaker = os.path.join( basefolder, "fmpimport")


</t>
<t tx="karstenw.20230521225929.5">def handleDataArchive( zipfilepath, extractdir ):
    """Obsolete. Switched to single .gz files due to 100MB limit for github."""

    with zipfile.ZipFile( zipfilepath ) as archivezip:
        zipmembers = archivezip.infolist()
        for zipmember in zipmembers:
            filename = zipmember.filename
            if filename.startswith('_'):
                print("SKIPPED ZIFILEMEMBER:", filename)
                continue
            basename, ext = os.path.splitext( filename )
            if ext not in (".sqlite3", ): #".tab", 
                print("SKIPPED:", filename)
                continue
            zipmember.filename = zipmember.filename.replace( "data/", "")
            print("EXTRACT zipfilename:", zipmember.filename )
            archivezip.extract( zipmember, extractdir )
    print("EXTRACT DONE!")


</t>
<t tx="karstenw.20230521225929.6">def readstatic( path ):
    """read a tabtext or gzipped tabtext export.
    
    Yield per record
    """
    path = os.path.abspath( path )
    folder, filename = os.path.split( path )
    basename, ext = os.path.splitext( filename )

    if ext == ".gz":
        # check the gzip file for .tab
        if basename.endswith(".tab"):
            f = gzip.open(path, 'rt', encoding="utf-8")
        else:
            return 0
    elif ext == ".tab":
        f = io.open(path, 'r', encoding="utf-8")
    else:
        return 0
    i = 0
    for line in f:
        items = tabline2items( line )
        yield items
        i += 1
    return i

</t>
<t tx="karstenw.20230521225929.7">def importConceptnetTables( importfiles ):
    total = time.time()    
    # side effect - create sqlite database and fill it with the
    # constant tables (language, relation, context)
    conn = getconnection( databasefile )
    
    bucketsize = 100000
    
    def emptyBucket(conn, bucket, tablename):
        c = conn.cursor()
        insert = 'INSERT INTO "%s" VALUES (?,?,?,?,?);' % (tablename,)
        c.executemany( insert, bucket )
        commit( conn )
    
    bucket = []
    
    # pdb.set_trace()
    
    for name in importfiles:
        start = time.time()
        i = 0
        folder, filename = os.path.split( name )
        basename, ext = os.path.splitext( filename )
        
        if '_' in basename:
            tablename = basename.split('_')[0]
        else:
            # use this - there are multiple dots in there
            tablename = filename.split( '.' )[0]
        
        print()
        print("tablename:", tablename)
        print(name)
        print()
        
        fieldnames = getTableFieldnames( conn, tablename )
        for items in readstatic( name ):
            # record = dict(zip(fieldnames, items) )
            # createRecord( conn, tablename, record, docommit=False )
            record = items
            bucket.append( record )
            i += 1
            if i % bucketsize == 0:
                emptyBucket( conn, bucket, tablename )
                bucket = []
                if not nb:
                    dotprinter(i, bucketsize)
        emptyBucket(conn, bucket, tablename)
        bucket = []
        commit( conn )
        stop = time.time()
        print("\nImport %s / %i records in %.3f" % (tablename, i, stop-start) ) 

    indices = (
        "CREATE INDEX idx_idconcept on concept (idconcept);",
        "CREATE INDEX idx_language on concept (languagecode);",
        "CREATE INDEX idx_concept on concept (concept);",
        "CREATE INDEX idx_context on concept (context);",
        
        # "CREATE INDEX idx_idedge  on edge (idedge);",
        "CREATE INDEX idx_concept1id  on edge (concept1id);",
        "CREATE INDEX idx_concept2id  on edge (concept2id);",
        "CREATE INDEX idx_weight  on edge (weight);"
    )
    c = conn.cursor()
    for index in indices:
        start = time.time()
        insert = 'INSERT INTO "%s" VALUES (?,?,?,?,?);' % (tablename,)
        c.execute(  index )
        commit( conn )
        stop = time.time()
        print("\n%s    in %.3f" % (index, stop-start) )
    print("\nImport CONCEPTNET-LITE into sqlite in %.3fs" % (time.time()-total,) ) 


</t>
<t tx="karstenw.20230521225929.8"></t>
<t tx="karstenw.20230521225929.9">def dotprinter( count, scale=1000, lineitems=100 ):
    """Non-interactive terminal video game ;-)"""

    # how many counted things ( count) per line
    line = scale * lineitems

    # make an empty line every 5 lines
    block = line * 5

    sys.stdout.write(".")
    if count % line == 0:
        # end of line; print count up to here
        sys.stdout.write( f"  {count:,}" )
        sys.stdout.write("\n")
        if count % block == 0:
            sys.stdout.write("\n")
    sys.stdout.flush()


</t>
<t tx="karstenw.20230524124241.1">@language python
@tabwidth -4
@others
</t>
<t tx="karstenw.20230524124307.1">
"""The name Flowerword came from the first implementation inside the flowerewolf library. Just a collection of that missing 'en' functions.

The name stuck.
"""



import time
import io

kwdbg = 1
kwlog = 1

import pdb
import pprint
pp = pprint.pprint

# seed(1)

# need to import linguistics first - sets up sys.path and corpus/data folders for the sublibs

start = time.time()

import linguistics

import pattern
import pattern.text
import pattern.text.en as en
wordnet = en.wordnet


if 0:
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


stop = time.time()
if kwlog:
    print("FlowerWord imports: %.3f" % (stop-start,)  )



# synonym = a word that is similar in meaning,
# hypernym = a word with a broader meaning,       (tree =&gt; plant)
# hyponym = a word with a more specific meaning, (tree =&gt; oak)
# holonym = a word that is the whole of parts,   (tree =&gt; forest)
# meronym = a word that is a part of the whole,  (tree =&gt; trunk)
# antonym = a word that is opposite in meaning.

</t>
<t tx="karstenw.20230524124417.1">class FlowerWord:
    @others
</t>
<t tx="karstenw.20230524124417.2">def __init__(self, word):
    # pdb.set_trace()
    self.word = word
    self.synset = None
    self.synsets = wordnet.synsets( word )
    #word = word.replace("_", " ")
    self.idx = 0
    
    self.antonym = ""
    self.gloss = ""
    self.synonyms = []
    self.lexname = ""
    self.ic = 0.0
    
    
    if len(self.synsets) &gt; 0:
        self.synset = self.synsets[0]
        self.synonyms = self.synset.synonyms
        self.antonym = self.synset.antonym
        self.gloss = self.synset.gloss
        self.lexname = self.synset.lexname
        self.ic = self.synset.ic

</t>
<t tx="karstenw.20230524124417.3">def hyponyms(self):
    result = []
    for synset in self.synsets:
        hyponyms = synset.hyponyms()
        for hyponym in hyponyms:
            synonyms = hyponym.synonyms
            for synonym in synonyms:
                #synonym = synonym.replace("_", " ")
                result.append( synonym )
    result = list(set(result))
    return result

</t>
<t tx="karstenw.20230524124417.4">def hypernyms(self):
    result = []
    for synset in self.synsets:
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            synonyms = hypernym.synonyms
            for synonym in synonyms:
                #synonym = synonym.replace("_", " ")
                result.append( synonym )
    result = list(set(result))
    return result


</t>
<t tx="karstenw.20230524124417.5">def senses(self):
    result = []
    filter = set()
    for synset in self.synsets:
        senses = synset.senses
        for sense in senses:
            #sense = sense.replace("_", " ")
            if sense not in filter:
                # print("FlowerWord.senses()", sense )
                filter.add( sense )
                result.append( sense )
    # print("FlowerWord.senses()", result )
    return result


</t>
<t tx="karstenw.20230524124417.6">def holonyms(self):
    result = []
    for synset in self.synsets:
        holonyms = synset.holonyms()
        for holonym in holonyms:
            synonyms = holonym.synonyms
            for synonym in synonyms:
                #synonym = synonym.replace("_", " ")
                result.append( synonym )
    result = list(set(result))
    return result


</t>
<t tx="karstenw.20230524124417.7">def meronyms(self):
    result = []
    for synset in self.synsets:
        meronyms = synset.meronyms()
        for meronym in meronyms:
            synonyms = meronym.synonyms
            for synonym in synonyms:
                #synonym = synonym.replace("_", " ")
                result.append( synonym )
    result = list(set(result))
    return result


</t>
<t tx="karstenw.20260222150150.1"># py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

</t>
<t tx="karstenw.20260222150155.1">def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    """Make input string normalized unicode."""
    
    if type(s) not in (pstr, punicode):
        # apart from str/unicode/bytes we just need the repr
        s = str( s )
    if type(s) != punicode:
        s = punicode(s, srcencoding)
    s = unicodedata.normalize(normalizer, s)
    return s


</t>
<t tx="karstenw.20260222150200.1">def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
    """Make an ISO datestring."""
    if not dt:
        now = str(datetime.datetime.now())
    else:
        now = str(dt)
    if not dateonly:
        now = now[:19]
    else:
        now = now[:10]
    if nospaces:
        now = now.replace(" ", "_")
    if nocolons:
        now = now.replace(":", "")
    return now

</t>
<t tx="karstenw.20260501093741.1">def print(self):
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


</t>
<t tx="karstenw.20260606162533.1">start = time.time()


# handle regular python / Nodebox
nb=True
try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    nb=False
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

if kwdbg:
    print("PACKAGE_DIR:", PACKAGE_DIR)

PARENT_DIR, _ = os.path.split( PACKAGE_DIR )
DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )

if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

sys.path.insert(0, PACKAGE_DIR)

# pdb.set_trace()

# if run from Nodebox do not accumulate endless messages...
# therefore 
#       quiet=nb
# or
#       progress_handler=pg

# textblob uses nltk
if 1:
    import nltk
    nltk_data_dir = os.path.join( DATA_DIR, 'nltk-data' )
    nltk.data.path = [ nltk_data_dir ]

    nltk.download( "wordnet", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet_ic", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "sentiwordnet", download_dir=nltk_data_dir, quiet=nb )

    nltk.download( "wordnet2021", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet2022", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "wordnet31", download_dir=nltk_data_dir, quiet=nb )


    # textblob minimal downloads
    # wordnet already loaded
    nltk.download( "brown", download_dir=nltk_data_dir, quiet=nb )
    #nltk.download( "punkt", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "punkt_tab", download_dir=nltk_data_dir, quiet=nb )
    #nltk.download( "averaged_perceptron_tagger", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "averaged_perceptron_tagger_eng", download_dir=nltk_data_dir, quiet=nb )

    # textblob additional
    nltk.download( "conll2000", download_dir=nltk_data_dir, quiet=nb )
    nltk.download( "movie_reviews", download_dir=nltk_data_dir, quiet=nb )


import wn
from wn.util import ProgressHandler, ProgressBar

pg = ProgressBar
if nb:
    pg = ProgressHandler
wn.config.data_directory = os.path.join( DATA_DIR, 'wn-data' )

# https://github.com/omwn - open multilingual wordnet
wn.download("omw", add=True, progress_handler=pg)

# https://github.com/hdaSprachtechnologie/odenet - open german wordnet
wn.download("odenet", add=True, progress_handler=pg)

# https://github.com/globalwordnet/cili/ - collaborative interlingual index
wn.download("cili", add=True, progress_handler=pg)

stop = time.time()
print("nltk &amp; wn in %.3fsec" % (stop-start,) )
</t>
<t tx="karstenw.20260606163051.1">def handleResult( items ):
    pass

</t>
<t tx="karstenw.20260606163217.1"># directory init
#
# set data path "linguistics-data"
#
# insert current directory into sys.path

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR, _ = os.path.split( PACKAGE_DIR )

if kwlog:
    print("PACKAGE_DIR:", PACKAGE_DIR)

DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )

if kwlog:
    print("DATA_DIR:", DATA_DIR)

if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)


fullinit = False

</t>
<t tx="karstenw.20260628144829.1">if fullinit:
    import FlowerWord
    
    
    if kwlog:
        end_time = time.time()
        print("SYS import FlowerWord: %.3f" % (end_time - FlowerWord_time)  )
        print("SYS import linguistics: %.3f" % (end_time - init_time)  )

</t>
</tnodes>
</leo_file>
