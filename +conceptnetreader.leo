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
<v t="karstenw.20230316191437.2" a="E"><vh>conceptnetreader</vh>
<v t="karstenw.20230412164348.1" a="E"><vh>@clean conceptnetreader/__init__.py</vh>
<v t="karstenw.20230412164348.2"><vh>Declarations</vh></v>
<v t="karstenw.20230412164348.3"><vh>+ GLOBALS</vh></v>
<v t="karstenw.20230412164348.18"><vh>+ DB DEF +</vh></v>
<v t="karstenw.20260222152934.1"><vh>+ REDUCED LANGUAGESET +</vh></v>
<v t="karstenw.20230503151220.1"><vh>initlib</vh></v>
<v t="karstenw.20230503150110.1"><vh>+ CNR +</vh>
<v t="karstenw.20230503201353.1"><vh>getconcept</vh></v>
<v t="karstenw.20230504104816.1"><vh>getconceptByID</vh></v>
<v t="karstenw.20260222160914.1"><vh>getedges</vh></v>
<v t="karstenw.20230503150118.1"><vh>query_concept</vh></v>
<v t="karstenw.20260226103637.1"><vh>query_translations</vh></v>
<v t="karstenw.20260222145208.1"><vh>query_idlist</vh></v>
<v t="karstenw.20260222223643.1"><vh>filter_lang</vh></v>
<v t="karstenw.20260226103048.1"><vh>intOrIterable</vh></v>
</v>
<v t="karstenw.20230521140353.1" a="E"><vh>sdb</vh>
<v t="karstenw.20260222153130.1"><vh>tableItems</vh></v>
<v t="karstenw.20260224171849.1"><vh>+ GLOBALS +</vh></v>
<v t="karstenw.20230521140605.1"><vh>py3</vh></v>
<v t="karstenw.20230521140814.1"><vh>makeunicode</vh></v>
<v t="karstenw.20230521140804.1"><vh>datestring</vh></v>
<v t="karstenw.20230521140353.2"><vh>dotprinter</vh></v>
<v t="karstenw.20230521140353.3"><vh>tabline2items</vh></v>
<v t="karstenw.20230521140353.4"><vh>getconnection</vh></v>
<v t="karstenw.20260219155615.1"><vh>sqlcreatetable</vh></v>
<v t="karstenw.20260219160832.1"><vh>sqlcreateindices</vh></v>
<v t="karstenw.20260219160844.1"><vh>sqlcreatetriggers</vh></v>
<v t="karstenw.20260219155047.1"><vh>init_dbfile</vh></v>
<v t="karstenw.20230521140353.5"><vh>commit</vh></v>
<v t="karstenw.20230521140521.1"><vh>executeQuery</vh></v>
<v t="karstenw.20230521140353.6"><vh>dict_factory</vh></v>
<v t="karstenw.20260222154944.1"><vh>namedtuple_factory</vh></v>
<v t="karstenw.20230521140353.7"><vh>getTableFieldnames</vh></v>
<v t="karstenw.20230521140353.8"><vh>createStatement</vh></v>
<v t="karstenw.20230521140353.9"><vh>createRecord</vh></v>
<v t="karstenw.20230521140441.1"><vh>fetchAllRecords</vh></v>
</v>
</v>
<v t="karstenw.20260224231701.1" a="E"><vh>TRASH</vh>
<v t="karstenw.20230503212558.1"><vh>getedgesOLD</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230316191437.2"></t>
<t tx="karstenw.20230412164348.1">@language python
@tabwidth -4
@others

if os.path.exists( databasefile ):
    initlib()

if __name__ == "__main__":
    pass

</t>
<t tx="karstenw.20230412164348.18">database = {
    'relation': [
        ('idrelation',          'INTEGER PRIMARY KEY'),
        ('conceptnetrelation',  'TEXT'),
        ('patternrelation',     'TEXT'),
        ('symmetric',           'INT'),
        ('reverse',             'INT'),
        ('origrelation',        'INT')
    ],
    'concept': [
        ('idconcept',   'INTEGER PRIMARY KEY'),
        ('languagecode','TEXT'),
        ('concept',     'TEXT'),
        ('typ',         'TEXT'),
        # ('source',      'TEXT'),
        ('context',     'TEXT')
    ],
    'edge': [
        ('idedge',      'INTEGER PRIMARY KEY'),
        ('concept1id',  'INT'),
        ('relationid',  'INT'),
        ('concept2id',  'INT'),
        ('weight',      'DOUBLE')
    ],
    'language': [
        ('idlanguage',  'INTEGER PRIMARY KEY'),
        ('languagecode','TEXT'),
        ('languagename','TEXT'),
        ('autonym',     'TEXT'),
        ('include',     'INT')
    ],
    'context': [
        ('idcontext',   'INTEGER PRIMARY KEY'),
        ('context',     'TEXT')
    ],
}


</t>
<t tx="karstenw.20230412164348.2"># -*- coding: utf-8; -*-

from __future__ import print_function

import sys
import os

import time
import datetime

import sqlite3
import unicodedata

import json

import itertools

import functools

import collections
namedtuple = collections.namedtuple


import pdb
kwdbg = 0
kwlog = 0
kwerr = 0

import pprint
pp = pprint.pprint


def sortlistfunction(thelist, thecompare, reverse=False):
    if py3:
        sortkeyfunction = functools.cmp_to_key( thecompare )
        thelist.sort( key=sortkeyfunction, reverse=reverse )
    else:
        thelist.sort( thecompare, reverse=reverse )

</t>
<t tx="karstenw.20230412164348.3">analyzed = False

PACKAGE_DIR, _ = os.path.split( os.path.abspath( __file__ ) )
DATA_DIR = os.path.abspath( os.path.join( PACKAGE_DIR, '..', '..', 'linguistics-data', 'conceptnet-data' ) )

databasefile = os.path.join( DATA_DIR, "conceptnet.sqlite3")


# languagecode( e.g. 'en') -&gt; languagerecord
#  'de': {'autonym': 'Deutsch', 'idlanguage': 54, 'include': 3, 'languagecode': 'de', 'languagename': 'German'},
languages = {}
languagenames = {}

# id -&gt; {'idrelation': 1, 'conceptnetrelation': '/r/Antonym', 'patternrelation': 'is-opposite-of', 'symmetric': 1, 'reverse': 0}
relations = {}
relationnames = {}

# yet UNUSED
# context -&gt; idcontext
contexts = {}

inited = False

# cache loaded concepts
# id -&gt; concept
conceptCache = {}


</t>
<t tx="karstenw.20230503150110.1"></t>
<t tx="karstenw.20230503150118.1">def query_concept(  concept, relation=None, context=None,
                    maxedges=1000, lang="en", weight=0.6 ):
    """Retrieve a concept from the sqlite database.
    
    relation &amp; context are ignored in getedges.
    """

    conn = getconnection( databasefile)

    concept = concept.lower()
    concept = concept.replace("_", " ")
    lang = lang.lower()

    resultConcepts = []
    
    concepts = getconcept( conn, concept, "", lang )
    if not concepts:
        return concepts, resultConcepts, conceptCache

    # cache it
    conceptIDs = set()
    for concept in concepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    rawedges1, collectedConceptIDs1 = getedges( conn, conceptIDs,
                        maxedges=0, weight=weight )
    
    secondLoad = set()
    for conceptID in collectedConceptIDs1:
        if conceptID not in conceptCache:
            secondLoad.add( conceptID )
    
    missingConcepts = getconceptByID( conn, secondLoad )
    for concept in missingConcepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    for edge in rawedges1:
        idedge, concept1id, relationid, concept2id, weight = edge
        
        relationrecord = relations.get( relationid, {} )
        if not relationrecord:
            continue
        
        if relation is not None:
            if not intOrIterable(relationid, relation):
                continue
        
        relationname = relationrecord.get('patternrelation', "")
        
        concept1 = conceptCache[concept1id]
        cn1name = concept1.concept
        cn1lang = concept1.languagecode
        context1 = concept1.context
        
        concept2 = conceptCache[concept2id]
        cn2name = concept2.concept
        cn2lang = concept2.languagecode
        context2 = concept2.context
        
        if 1:
            if cn1lang not in coreLanguageCodes:
                #print("LANG DROPPED:", concept1)
                continue
            
            if cn2lang not in coreLanguageCodes:
                #print("LANG DROPPED:", concept2)
                continue
        
        record = FullConcept( idedge,
                              concept1id, cn1name, cn1lang, context1,
                              relationid, relationname, weight,
                              concept2id, cn2name, cn2lang, context2)
        resultConcepts.append( record )
    
    if maxedges &gt; 0:
        resultConcepts = resultConcepts[:maxedges]
    
    return concepts, resultConcepts, conceptCache


</t>
<t tx="karstenw.20230503151220.1">def initlib():
    """Init the library by loading languages, relations, contexts into globals."""

    global languages, relations, contexts, inited, languagenames, relationnames

    if not os.path.exists( databasefile ):
        return {},{},{}

    conn = getconnection( databasefile )

    old_factory = conn.row_factory
    conn.row_factory = dict_factory

    if inited:
        return languages, relations, contexts
    
    result = {}
    resultnames = {}
    records = fetchAllRecords(conn, "language")
    for record in records:
        languagecode = record['languagecode']
        languagename = record['languagename']
        result[languagecode] = record
        resultnames[languagename] = languagecode
    languages = result.copy()
    languagenames = resultnames.copy()

    result = {}
    resultnames = {}
    records = fetchAllRecords(conn, "relation")
    for record in records:
        idrelation = record['idrelation']
        patternrelation = record['patternrelation']
        if patternrelation != "":
            result[idrelation] = record
            resultnames[patternrelation] = idrelation
    relations = result.copy()
    relationnames = resultnames.copy()
    
    result = {}
    records = fetchAllRecords(conn, "context")
    for record in records:
        context = record['context']
        idcontext = record['idcontext']
        result[context] = idcontext
    contexts = result.copy()

    inited = True
    return languages, relations, contexts


</t>
<t tx="karstenw.20230503201353.1">def getconcept( conn, concept, context, lang, slack=False ):
    """Query the concept table."""

    query = ("SELECT idconcept,languagecode,concept,typ,context "
             "FROM concept "
             "WHERE concept=? " )
    
    searchvalues = [concept, ]
    
    if slack:
        query = ("SELECT idconcept,languagecode,concept,typ,context "
                 "FROM concept "
                 'WHERE concept like "?" ' )
        searchvalues.append( concept )
    
    if lang:
        query = query + ' AND languagecode=? '
        searchvalues.append( lang )
    
    if context:
        query = query + ' AND context like "?" '
        searchvalues.append( context )
    
    concepts = executeQuery(conn, query, searchvalues )
    
    result = []
    for concept in concepts:
        result.append(  ConceptRecord( *concept ) )

    return result


</t>
<t tx="karstenw.20230503212558.1">def getedgesOLD( conn, conceptid, relationIDs=False, maxedges=0, weight=0.0 ):
    """Query the edges for conceptID.
    
    Currently only queries the left entry / concept1, TODO
    
    Currently ignores the relationIDs parameter, which should be a list of relationIDs.
    
    """

    # fetch relations
    query = (
        "SELECT concept1id,relationid,concept2id,weight "
        "FROM edge "
        "WHERE concept1id=%i ")
    
    # if weight    
    if weight &gt; 0.0:
        query = query + "AND weight&gt;=%f "
    
    # sort result
    query = query + "ORDER BY weight DESC "
    
    # insert parameters
    query = query % ( conceptid, weight)

    # maxedges return 
    m = 0
    try:
        m = int(maxedges)
    except:
        pass
    if m &gt; 0:
        query = query + " LIMIT %i" % (m,)

    cursor = executeQuery(conn, query )
    edges = cursor.fetchall()

    weightlimit = weight
    result = []
    for edge in edges:
        concept1id,relationid,concept2id,weight = edge

        relation = relations.get( relationid, {} )
        if not relation:
            print("getedges(): missed relationID:", relationid)
            continue

        relationname = relation.get( 'patternrelation', "" )
        reverse = relation.get( 'reverse', 0 )
        symmetric = relation.get( 'symmetric', 0 )
        origrelation = relation.get( 'origrelation', 0 )

        if not relationname:
            continue

        # filter relations
        if relationIDs:
            if relationid not in relationIDs:
                continue
            if relationname:
                if relationname not in relationIDs:
                    continue
        
        result.append( (concept1id,relationname,concept2id,weight,reverse,symmetric) )
    return result


</t>
<t tx="karstenw.20230504104816.1">def getconceptByID( conn, conceptid ):
    """Retrieve concepts by ID. 
    conceptid  - either idconcept or listtype of idconcept.
    
    returns list of ConceptRecord.
    """
    
    old_factory = conn.row_factory
    conn.row_factory = namedtuple_factory

    query = ("SELECT idconcept,languagecode,concept,typ,context "
             "FROM concept "
             "WHERE idconcept=%s;" % (str(conceptid),))
    
    if type(conceptid) in (list, tuple, set):
        # make sorted idlist
        conceptid = list(conceptid)
        conceptid.sort()
        conceptidstr = [str(i) for i in conceptid]
        sqlfileids = ','.join( conceptidstr )
        query = ("SELECT idconcept,languagecode,concept,typ,context "
                 "FROM concept "
                 "WHERE idconcept in (%s);" % (sqlfileids,) )
    concepts = executeQuery(conn, query ).fetchall()
    conn.row_factory = old_factory
    return concepts


</t>
<t tx="karstenw.20230521140353.1">################################################################################

#
# Parts of the former sdb (simple database library)
# which was merged into filepool
# which is not ready for the world
#
# i.e. my collection of sqlite helpers
#
#


</t>
<t tx="karstenw.20230521140353.2">def dotprinter( count, scale=1000, lineitems=100 ):
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
<t tx="karstenw.20230521140353.3">def tabline2items( line ):
    line = line.strip(" \r\n")
    line = makeunicode( line )
    items = line.split( u"\t" )
    return items


</t>
<t tx="karstenw.20230521140353.4">def getconnection( filepath, doinit=0, database={} ):
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
    
    if doinit:
        init_dbfile( conn, database )
    return conn


</t>
<t tx="karstenw.20230521140353.5">def commit( conn ):
    ok = False
    i = 0
    while not ok:
        if i &gt; 20:
            break
        try:
            conn.commit()
            ok = True
        except sqlite3.OperationalError as err:
            print("")   # debugprint
            print( "ERR: " + repr(err) )
            time.sleep( 0.01 )
            i += 1


</t>
<t tx="karstenw.20230521140353.6">def dict_factory(cursor, row):
    # from pysqlite code examples
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


</t>
<t tx="karstenw.20230521140353.7">def getTableFieldnames(conn, tablename):

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
<t tx="karstenw.20230521140353.8">def createStatement( tablename, fieldnames ):
    """
    Create SELECT, INSERT and UPDATE statements from tablename and
    fieldname list.
    """
    u = u"UPDATE %s SET " % (tablename,)
    nkeys = len(fieldnames)
    
    lfieldnames = u",".join(fieldnames)
    ifieldnames = u'(' + lfieldnames + u')'
    qfieldnames = lfieldnames
    
    repmarks = [u'?'] * nkeys
    repmarks = u','.join( repmarks )
    
    q = "SELECT (%s) FROM %s" % ( lfieldnames, tablename )
    if nkeys &gt; 1:
        q = "SELECT %s FROM %s" % ( lfieldnames, tablename )
    
    i = "INSERT INTO %s (%s) VALUES (%s)" % ( tablename, lfieldnames, repmarks)
    
    ufielditems = []
    s = u"%s=?"
    for f in fieldnames:
        ufielditems.append( s % f )
    ufieldnames = u",".join( ufielditems )
    u = u + ufieldnames
    
    result = []
    return (q,i,u)


</t>
<t tx="karstenw.20230521140353.9">def createRecord( conn, tablename, recordDict, docommit=True):
    
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
<t tx="karstenw.20230521140441.1">def fetchAllRecords(conn, tablename, sort1="", sort1dir="ASC",  sort2="", sort2dir="ASC"):
    """Return a list with all record dicts from table tablename."""
    
    result = []
    
    old_factory = conn.row_factory
    conn.row_factory = dict_factory
    
    fieldnames = getTableFieldnames(conn, tablename)
    q, _, _ = createStatement( tablename, fieldnames )
    
    if sort1:
        q = q + u" ORDER BY %s %s" % (sort1, sort1dir)
        
        if sort2:
            q = q + u", %s %s" % (sort2, sort2dir)
    
    cursor = executeQuery(conn, q)
    result = cursor.fetchall()
    
    conn.row_factory = old_factory
    return result


</t>
<t tx="karstenw.20230521140521.1">def executeQuery(conn, query, values=False, many=False):
    """Catch a query on a locked database."""
    query = makeunicode( query )
    if 0: #kwlog:
        print( "executeQuery( '%s' )" % bquery )    # debugprint
        
    if values == False:
        values = []

    cursor = conn.cursor()
    count = 0
    ok = error = False
    last = 0
    while not ok:
        try:
            if many:
                last = cursor.executemany( query, values )
            else:
                last = cursor.execute( query, values )
            ok = True
        except sqlite3.OperationalError as v:
            print("query:", query)
            print( v )  # debugprint
            error = True
            time.sleep(0.1)
            count += 1
            if count &gt; 10:
                break
    if error and count:
        pass
    return cursor


</t>
<t tx="karstenw.20230521140605.1"># py3 stuff
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
<t tx="karstenw.20230521140804.1">def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
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
<t tx="karstenw.20230521140814.1">def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    """Make input string normalized unicode."""
    
    if type(s) not in (pstr, punicode):
        # apart from str/unicode/bytes we just need the repr
        s = str( s )
    if type(s) != punicode:
        s = punicode(s, srcencoding)
    s = unicodedata.normalize(normalizer, s)
    return s


</t>
<t tx="karstenw.20260219155047.1">def init_dbfile( connection, database, dotriggersandindices=False ):
    result = []

    # update this to current status first
    c = connection.cursor()

    for table in database.keys():
        drop = u"DROP TABLE IF EXISTS %s;" % (table,)
        c.execute( drop )

        sql = sqlcreatetable(database, table)
        c.execute( sql )

        for trigger in sqlcreatetriggers(database, table):
            if trigger:
                if dotriggersandindices:
                    c.execute( trigger )
                result.append( trigger )

        for index in sqlcreateindices(database, table):
            if index:
                if dotriggersandindices:
                    c.execute( index )
                result.append( index )

    commit( connection )
    c.close()
    return result
</t>
<t tx="karstenw.20260219155615.1">def sqlcreatetable(db, tablename):

    items = db.get(tablename, False)
    
    if not items:
        return False
    
    c1 = 'CREATE TABLE "%s" (' % (tablename,)
    cn = ');'
    t = tablename

    l = []
    for item in items:
        name,typ = item
        name = makeunicode(name)
        s = u'\t%s %s' % (name,typ)
        l.append(s)
    s = u",\n".join(l)
    return u"\n".join( (c1,s,cn) )

</t>
<t tx="karstenw.20260219160832.1">def sqlcreateindices(db, tablename):
    return []


</t>
<t tx="karstenw.20260219160844.1">def sqlcreatetriggers(db, tablename):
    return []
</t>
<t tx="karstenw.20260222145208.1">def query_idlist( conn, tablename, idfieldname, idlist ):
    """Retrieve all fields from a table tablename where `idfieldname` 
    contains the elenemts from idlist.
    
    Returns list of (EdgeRecord, ConceptRecord or AdhocRecord)
    """
    
    result = []
    
    if kwdbg:
        print("query_idlist( %s, %s )" % (tablename, idfieldname))
    
    # collect SELECT fieldnames
    if tablename == "edge":
        fieldnames = edgenames
        Record = EdgeRecord
    elif tablename == "concept":
        fieldnames = conceptnames
        Record = ConceptRecord
    else:
        print("ILLEGAL TABLENAME:", tablename)
        fieldnames, _ = tableItems(database, tablename)
        classname = tablename.capitalize() + "Record"
        Record = namedtuple( classname, fieldnames )
        if kwdbg:
            pdb.set_trace()
            print("Please check created Record class...")
    
    fieldnamesselect = ','.join( fieldnames )
    
    # collect SELECT ... in (IDVALUES...)
    intIDs = [int(i) for i in idlist]
    intIDs.sort()
    fileidstr = [str(i) for i in intIDs]
    sqlfileids = ','.join( fileidstr )
    
    q = ( "SELECT %s "
          "FROM %s "
          "WHERE %s IN (%s);")
    q = q % ( fieldnamesselect, tablename, idfieldname, sqlfileids )
    
    if kwdbg:
        print("query_idlist()")
        print( q )
    
    records = executeQuery( conn, q )
    
    # pdb.set_trace()
    
    for record in records:
        namedrecord = Record( *record )
        result.append( namedrecord )
    
    return result


</t>
<t tx="karstenw.20260222152934.1">reducedLanguages = set( (
    "af ang bg br ca ce co cop crh cs cu cy da de dlm dum el en enm eo es et eu fi "
    "fo fr frk frm fro frp frr fur fy ga gd gl gmh gml goh got gsw haw hit ht hu ia "
    "ie is it ku kw la lb li lij lmo mga mi mul nap nds nl no non nrf oc odt ofs oge "
    "osp osx ota pcd pl pms prg pro pt ro roa-opt sc scn sco se sga sh sk sl stq sv "
    "szl tr twf vec wa yi").split() )


coreLanguageCodes = set( (
    "en fr it de es ru pt nl da cs sv ro la"
).split() )


# UNUSED
myLanguages = set( (
    "en fr it de es nl ru pt ja zh"
    # old english
    "ang cy enm ga gd mga osx sco sga "
    # old german
    "gmh gml goh got gws nds prg yi "
    # old french
    "br co frk frm fro frp nrf pro "
    # old spanish
    "ca eu gl osp "
    # old italian
    "fur la lom nap ne vec sc scn "
).split() )

</t>
<t tx="karstenw.20260222153130.1">def tableItems( db, tablename):
    items = db.get(tablename, [])
    
    if not items:
        return [ [], [] ]
    
    fieldnames = []
    fieldtypes = []
    for item in items:
        fieldnames.append( item[0] )
        fieldtypes.append( item[1] )
    return (fieldnames, fieldtypes)


</t>
<t tx="karstenw.20260222154944.1"># UNTESTED
def namedtuple_factory(cursor, row):
    global RecordTypeNumber
    """Create a namedtuple class and return records with it."""
    fieldnames = [d[0] for d in cursor.description]
    namekey = ','.join( fieldnames )
    if namekey not in RecordNamedTupletypes:
        classname = "Record" + str(RecordTypeNumber)
        RecordTypeNumber += 1
        Record = namedtuple( classname, fieldnames )
        RecordNamedTupletypes[namekey] = Record
    else:
        Record = RecordNamedTupletypes[namekey]
    return Record( *row )


</t>
<t tx="karstenw.20260222160914.1">def getedges( conn, conceptIDs, relationIDs=None, maxedges=0, weight=0.0 ):
    """Query the edges for conceptID.
    
    Queries left and right concept entry.
    
    Currently ignores the relationIDs parameter, which should be a list of relationIDs.
    
    returns a list of EdgeRecord, set of idconcept
    """
    
    # fetch relations 
    edges = query_idlist( conn, "edge", "concept1id", conceptIDs)
    edges.extend( query_idlist( conn, "edge", "concept2id", conceptIDs) )
    
    # filter for weight
    if weight &gt; 0.0:
        edges = [rec for rec in edges if rec.weight &gt;= weight]
    
    # sort the edges
    def edgesort( a,b ):
        w1 = a.weight
        w2 = b.weight
        if w1 &gt; w2:
            return 1
        if w1 &lt; w2:
            return -1
        return 0
    sortlistfunction(edges, edgesort, reverse=True )
    
    collectedConceptIDs = set()
    result = []
    for edge in edges:
        
        # filter by relationIDs
        if relationIDs is not None:
            if edge.relationid not in relationIDs:
                continue

        collectedConceptIDs.add( edge.concept1id )
        collectedConceptIDs.add( edge.concept2id )
        result.append( edge )

    # reduce to maxedges
    if maxedges &gt; 0:
        if len(result) &gt; maxedges:
            result = result[:maxedges]
    
    return result, collectedConceptIDs


</t>
<t tx="karstenw.20260222223643.1">def filter_lang( concepts, lang1list, lang2list ):
    """From a list of ConceptRecords drop all those whose languagecode
       is not in lang1list/lang2list.
    """
    result = []
    for concept in concepts:
        if concept.concept1lang in lang1list:
            if concept.concept2lang in lang2list:
                result.append( concept )
    return result


</t>
<t tx="karstenw.20260224171849.1">RecordNamedTupletypes = {}
RecordTypeNumber = 1


conceptnames, _ = tableItems(database, "concept")
ConceptRecord = namedtuple( 'ConceptRecord', conceptnames )

edgenames, _ = tableItems(database, "edge")
EdgeRecord = namedtuple( 'EdgeRecord', edgenames )

# idedge concept1id cn1name cn1lang  context1 relationid relationname concept2id cn2name cn2lang context2 weight 
fullconceptnames = (
        "idedge "
        "concept1id concept1name concept1lang concept1context "
        "relationid relationname weight "
        "concept2id concept2name concept2lang concept2context")
fullconceptnames = fullconceptnames.split()
FullConcept = namedtuple( 'FullConcept', fullconceptnames )


key = ','.join( conceptnames )
RecordNamedTupletypes[key] = ConceptRecord

key = ','.join( edgenames )
RecordNamedTupletypes[key] = EdgeRecord

key = ','.join( fullconceptnames )
RecordNamedTupletypes[key] = FullConcept




</t>
<t tx="karstenw.20260224231701.1"></t>
<t tx="karstenw.20260226103048.1">def intOrIterable( value, argument ):
    """Check if value is either equal to argument or contained in argument"""
    if type( argument ) in (int, float, str, bytes):
        return value == argument
    return value in argument


</t>
<t tx="karstenw.20260226103637.1">def query_translations( concept, lang, weight=0.6, maxedges=0 ):
    """Retrieve translations for a concept."""

    conn = getconnection( databasefile)

    concept = concept.lower()
    concept = concept.replace("_", " ")
    lang = lang.lower()
    
    concepts = []
    resultConcepts = []
    
    concepts = getconcept( conn, concept, "", lang )
    if not concepts:
        return concepts, resultConcepts
    
    initialConcept = concepts[0]
    
    # cache it
    conceptIDs = set()
    for concept in concepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    rawedges1, collectedConceptIDs1 = getedges( conn, conceptIDs,
                                                maxedges=0, weight=weight )
    secondLoad = set()
    for conceptID in collectedConceptIDs1:
        if conceptID not in conceptCache:
            secondLoad.add( conceptID )
    
    missingConcepts = getconceptByID( conn, secondLoad )
    for concept in missingConcepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    relationname = "is-same-as"
    wantedrelationid = relationnames.get( relationname, None )
    
    
    doubletten = set()
    for edge in rawedges1:
        idedge, concept1id, relationid, concept2id, weight = edge
        if wantedrelationid != relationid:
            continue
        
        # if searchconcept is not first place, swap
        if concept2id  == initialConcept.idconcept:
            concept1id, concept2id = concept2id, concept1id
        
        if (concept1id, concept2id) in doubletten:
            continue
        doubletten.add( (concept1id, concept2id) )
        
        concept1 = conceptCache[concept1id]
        cn1name = concept1.concept
        cn1lang = concept1.languagecode
        context1 = concept1.context
        
        concept2 = conceptCache[concept2id]
        cn2name = concept2.concept
        cn2lang = concept2.languagecode
        context2 = concept2.context
        
        # we want the other languages
        if concept2.languagecode == concept1.languagecode:
            continue
        
        record = FullConcept( idedge,
                              concept1id, cn1name, cn1lang, context1,
                              relationid, relationname, weight,
                              concept2id, cn2name, cn2lang, context2)
        resultConcepts.append( record )
    
    if maxedges &gt; 0:
        resultConcepts = resultConcepts[:maxedges]
    
    return concepts, resultConcepts


</t>
</tnodes>
</leo_file>
