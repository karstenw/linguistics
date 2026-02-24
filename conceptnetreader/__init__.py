# -*- coding: utf-8; -*-

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

analyzed = False

PACKAGE_DIR, _ = os.path.split( os.path.abspath( __file__ ) )
DATA_DIR = os.path.abspath( os.path.join( PACKAGE_DIR, '..', '..', 'linguistics-data', 'conceptnet-data' ) )

databasefile = os.path.join( DATA_DIR, "conceptnet.sqlite3")


# languagecode( e.g. 'en') -> languagerecord
#  'de': {'autonym': 'Deutsch', 'idlanguage': 54, 'include': 3, 'languagecode': 'de', 'languagename': 'German'},
languages = {}


# id -> {'idrelation': 1, 'conceptnetrelation': '/r/Antonym', 'patternrelation': 'is-opposite-of', 'symmetric': 1, 'reverse': 0}
relations = {}


# yet UNUSED
# context -> idcontext
contexts = {}

inited = False


database = {
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


def tableItems( db, tablename):
    items = db.get(tablename, [])
    
    if not items:
        return [ [], [] ]

    fieldnames = []
    fieldtypes = []
    for item in items:
        fieldnames.append( item[0] )
        fieldtypes.append( item[1] )
    return (fieldnames, fieldtypes)


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
FullConcept = namedtuple( 'FullConcept', fullconceptnames )


def initlib():
    """Init the library by loading languages, relations, contexts into globals."""

    global languages, relations, contexts, inited

    if not os.path.exists( databasefile ):
        return {},{},{}

    conn = getconnection( databasefile )

    old_factory = conn.row_factory
    conn.row_factory = dict_factory

    if inited:
        return languages, relations, contexts
    
    result = {}
    records = fetchAllRecords(conn, "language")
    for record in records:
        languagecode = record['languagecode']
        result[languagecode] = record
    languages = result.copy()

    result = {}
    records = fetchAllRecords(conn, "relation")
    for record in records:
        idrelation = record['idrelation']
        patternrelation = record['patternrelation']
        if patternrelation != "":
            result[idrelation] = record
    relations = result.copy()

    result = {}
    records = fetchAllRecords(conn, "context")
    for record in records:
        context = record['context']
        idcontext = record['idcontext']
        result[context] = idcontext
    contexts = result.copy()

    inited = True
    return languages, relations, contexts


def getconcept( conn, concept, context, lang, relation, slack=False ):
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
    
    
    if 0: #relation:
        query = query + " AND relation  in (%s) " % (relation,)

    concepts = executeQuery(conn, query, searchvalues )
    # concepts = cursor.fetchall()
    
    result = []
    for concept in concepts:
        result.append(  ConceptRecord( *concept ) )

    return result


def getconceptByID( conn, conceptid ):
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


def getedges( conn, conceptIDs, relationIDs=False, maxedges=0, weight=0.0 ):
    """Query the edges for conceptID.
    
    Queries left and right concept entry.
    
    Currently ignores the relationIDs parameter, which should be a list of relationIDs.
    
    returns a list of EdgeRecord, set of idconcept
    """
    
    # fetch relations 
    edges = query_idlist( conn, "edge", "concept1id", conceptIDs)
    edges.extend( query_idlist( conn, "edge", "concept2id", conceptIDs) )
    
    # filter for weight
    if weight > 0.0:
        edges = [rec for rec in edges if rec.weight >= weight]
    
    # sort the edges
    def edgesort( a,b ):
        w1 = a.weight
        w2 = b.weight
        if w1 > w2:
            return 1
        if w1 < w2:
            return -1
        return 0
    sortlistfunction(edges, edgesort, reverse=True )
    
    # reduce to maxedges
    if maxedges > 0:
        edges = edges[:maxedges]
    
    collectedConceptIDs = set()
    result = []
    for edge in edges:
        
        # relationname ist UNUSED here
        if 0:
            # get relationname
            relation = relations.get( edge.relationid, {} )
            if not relation:
                print("getedges(): missed relationID:", edge)
                continue
            relationname = relation.get( 'patternrelation', "" )
            if not relationname:
                print("getedges(): missed relationName:", edge)
                continue

        collectedConceptIDs.add( edge.concept1id )
        collectedConceptIDs.add( edge.concept2id )
        result.append( edge )
    return result, collectedConceptIDs


def query_concept( concept, relation=None, context=None, maxedges=1000, lang="en", weight=0.6 ):
    """Retrieve a concept from the sqlite database.
    
    relation & context are ignored in getedges.
    """

    conn = getconnection( databasefile)

    concept = concept.lower()
    concept = concept.replace("_", " ")
    lang = lang.lower()

    # caching currently only per run
    conceptCache = {}
    
    concepts = []
    resultConcepts = []
    
    concepts = getconcept( conn, concept, context, lang, relation )
    if not concepts:
        return concepts, resultConcepts, conceptCache

    # cache it
    conceptIDs = set()
    for concept in concepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    rawedges1, collectedConceptIDs1 = getedges( conn, conceptIDs, [], maxedges=maxedges, weight=weight )
    if kwdbg:
        print("len(rawedges)", len(rawedges1) )
        print("len(collectedConceptIDs)", len(collectedConceptIDs1))
        print("107711 in collectedConceptIDs:", 107711 in collectedConceptIDs1 )
    secondLoad = set()
    for conceptID in collectedConceptIDs1:
        if conceptID not in conceptCache:
            secondLoad.add( conceptID )
    
    missingConcepts = getconceptByID( conn, secondLoad )
    for concept in missingConcepts:
        idconcept = concept.idconcept
        conceptCache[idconcept] = concept
        conceptIDs.add(idconcept)
    
    if 0:
        # 2nd pass
        rawedges2, collectedConceptIDs2 = getedges( conn, conceptIDs, [], 0, weight )
        thirdLoad = set()
        for conceptID in collectedConceptIDs2:
            if conceptID not in conceptCache:
                thirdLoad.add( conceptID )
        missingConcepts = getconceptByID( conn, thirdLoad )
        for concept in missingConcepts:
            idconcept = concept.idconcept
            conceptCache[idconcept] = concept
            conceptIDs.add(idconcept)
    else:
        rawedges2 = rawedges1
    
    if maxedges > 0:
        rawedges2 = rawedges2[:maxedges]
    
    for edge in rawedges2:
        idedge, concept1id, relationid, concept2id, weight = edge
        relation = relations.get( edge.relationid, {} )
        relationname = relation.get('patternrelation', "")
        
        concept1 = conceptCache[concept1id]
        cn1name = concept1.concept
        cn1lang = concept1.languagecode
        context1 = concept1.context

        concept2 = conceptCache[concept2id]
        cn2name = concept2.concept
        cn2lang = concept2.languagecode
        context2 = concept2.context
        
        record = FullConcept( idedge,
                              concept1id, cn1name, cn1lang, context1,
                              relationid, relationname, weight,
                              concept2id, cn2name, cn2lang, context2)
        resultConcepts.append( record )
        
    return concepts, resultConcepts, conceptCache


def query_idlist( conn, tablename, idfieldname, idlist ):
    
    """Retrieve all fields from a table tablename where `idfieldname` 
    contains the elenemts from idlist.
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


def filter_lang( concepts, lang1list, lang2list ):
    result = []
    for concept in concepts:
        if concept.concept1lang in lang1list:
            if concept.concept2lang in lang2list:
                result.append( concept )
    return result


RecordNamedTupletypes = {}
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
#RecordNamedTupletypes[key] = ConceptRecord

key = ','.join( edgenames )
#RecordNamedTupletypes[key] = EdgeRecord

key = ','.join( fullconceptnames )
#RecordNamedTupletypes[key] = FullConcept

# py3 stuff
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

def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    """Make input string normalized unicode."""
    
    if type(s) not in (pstr, punicode):
        # apart from str/unicode/bytes we just need the repr
        s = str( s )
    if type(s) != punicode:
        s = punicode(s, srcencoding)
    s = unicodedata.normalize(normalizer, s)
    return s


def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
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

def dotprinter( count, scale=1000, lineitems=100 ):
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


def tabline2items( line ):
    line = line.strip(" \r\n")
    line = makeunicode( line )
    items = line.split( u"\t" )
    return items


def getconnection( filepath, doinit=0, database={} ):
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


def sqlcreatetable(db, tablename):

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

def sqlcreateindices(db, tablename):
    return []


def sqlcreatetriggers(db, tablename):
    return []
def init_dbfile( connection, database, dotriggersandindices=False ):
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
def commit( conn ):
    ok = False
    i = 0
    while not ok:
        if i > 20:
            break
        try:
            conn.commit()
            ok = True
        except sqlite3.OperationalError as err:
            print("")   # debugprint
            print( "ERR: " + repr(err) )
            time.sleep( 0.01 )
            i += 1


def executeQuery(conn, query, values=False, many=False):
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
            if count > 10:
                break
    if error and count:
        pass
    return cursor


def dict_factory(cursor, row):
    # from pysqlite code examples
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# UNTESTED
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


def getTableFieldnames(conn, tablename):

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


def createStatement( tablename, fieldnames ):
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
    if nkeys > 1:
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


def createRecord( conn, tablename, recordDict, docommit=True):

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


def fetchAllRecords(conn, tablename, sort1="", sort1dir="ASC",  sort2="", sort2dir="ASC"):
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


# see RECORDS

if __name__ == "__main__":
    pass

if os.path.exists( databasefile ):
    initlib()


