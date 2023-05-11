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
<v t="karstenw.20230412164348.1"><vh>@clean conceptnetreader/__init__.py</vh>
<v t="karstenw.20230412164348.2"><vh>Declarations</vh></v>
<v t="karstenw.20230412164348.3"><vh>+ GLOBALS</vh></v>
<v t="karstenw.20230503151220.1"><vh>initlib</vh></v>
<v t="karstenw.20230412164348.18"><vh>+ DB DEF +</vh></v>
<v t="karstenw.20230503150110.1" a="E"><vh>+ CNR +</vh>
<v t="karstenw.20230503201353.1"><vh>getconcept</vh></v>
<v t="karstenw.20230504104816.1"><vh>getconceptByID</vh></v>
<v t="karstenw.20230503212558.1"><vh>getedges</vh></v>
<v t="karstenw.20230503150118.1"><vh>query_concept</vh></v>
</v>
</v>
<v t="karstenw.20230511095450.1" a="E"><vh>@clean install-conceptnet-database.py</vh>
<v t="karstenw.20230511095516.1"><vh>Declarations 1</vh></v>
<v t="karstenw.20230511095550.1"><vh>Globals</vh></v>
<v t="karstenw.20230511100003.1"><vh>handleDataArchive</vh></v>
<v t="karstenw.20230511121040.1"><vh>readstatic</vh></v>
<v t="karstenw.20230511095516.2"><vh>importConceptnetTables</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="karstenw.20230316191437.2"></t>
<t tx="karstenw.20230412164348.1">@language python
@tabwidth -4
@others
if __name__ == "__main__":
    pass


</t>
<t tx="karstenw.20230412164348.18">database = {
    'relation': [
        ('idrelation',          'INTEGER PRIMARY KEY'),
        ('conceptnetrelation',  'TEXT'),
        ('patternrelation',     'TEXT'),
        ('symmetric',           'INT'),
        ('reverse',             'INT')
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

import pdb
kwdbg = 1
kwlog = 1
kwerr = 1

import pprint
pp = pprint.pprint

import sdb
makeunicode = sdb.makeunicode
fetchAllRecords = sdb.fetchAllRecords
dict_factory = sdb.dict_factory
getconnection = sdb.getconnection
executeQuery = sdb.executeQuery
commit = sdb.commit
dotprinter = sdb.dotprinter
createRecord = sdb.createRecord



</t>
<t tx="karstenw.20230412164348.3">analyzed = False

PACKAGE_DIR, _ = os.path.split( os.path.abspath( __file__ ) )
DATA_DIR = os.path.abspath( os.path.join( PACKAGE_DIR, '..', '..', 'linguistics-data', 'conceptnet-data' ) )

databasefile = os.path.abspath("./data/conceptnet.sqlite3")

languages = relations = contexts = ""

inited = False

</t>
<t tx="karstenw.20230503150110.1"></t>
<t tx="karstenw.20230503150118.1">def query_concept( concept, relation=None, context=None, maxedges=None, lang="en", weight=0.0 ):
    """Retrieve a concept from the sqlite database.
    
    relation &amp; context are ignored in getedges.
    """

    conn = getconnection( databasefile)

    concept = concept.lower()
    concept = concept.replace("_", " ")
    lang = lang.lower()

    # caching currently only per run
    loadedConcepts = {}
    concepts = []
    edges = []

    
    conceptIDs = []
    concepts = getconcept( conn, concept, context, lang, relation )
    if not concepts:
        return concepts, edges, loadedConcepts

    # cache it
    for concept in concepts:
        idconcept = concept['idconcept']
        loadedConcepts[idconcept] = concept
    rawedges = getedges( conn, concepts[0]['idconcept'], [], maxedges, weight )

    for rawedge in rawedges:
        cn1id, rel, cn2id, w, rev, sym = rawedge

        if cn1id not in loadedConcepts:
            cn1 = getconceptByID( conn, cn1id )
            loadedConcepts[cn1id] = cn1

        if cn2id not in loadedConcepts:
            cn2 = getconceptByID( conn, cn2id )
            loadedConcepts[cn2id] = cn2

        cn1name = loadedConcepts[cn1id].get('concept', '')
        cn1lang = loadedConcepts[cn1id].get('languagecode', '')

        cn2name = loadedConcepts[cn2id].get('concept', '')
        cn2lang = loadedConcepts[cn2id].get('languagecode', '')

        edges.append( (cn1lang,cn1name,rel,cn2lang,cn2name,w,rev,sym) )
        
    return concepts, edges, loadedConcepts


</t>
<t tx="karstenw.20230503151220.1">def initlib():
    """Init the library by loading languages, relations, contexts into globals."""

    global languages, relations, contexts, inited

    conn = getconnection( databasefile )

    # pdb.set_trace()

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


</t>
<t tx="karstenw.20230503201353.1">def getconcept( conn, concept, context, lang, relation, slack=False ):

    old_factory = conn.row_factory
    conn.row_factory = dict_factory

    query = ("SELECT idconcept,languagecode,concept,typ,context "
             "FROM concept "
             "WHERE concept=? AND languagecode=? " )
    if slack:
        query = ("SELECT idconcept,languagecode,concept,typ,context "
                 "FROM concept "
                 'WHERE concept like "?" ' )
        if lang:
            query = query + ' AND languagecode=? '

    searchvalues = [concept, lang]

    if context:
        query = query + " AND context=? "
        searchvalues.append( context )

    if relation:
        query = query + " AND relation  in (%s) " % (relation,)

    cursor = executeQuery(conn, query, searchvalues )
    concepts = cursor.fetchall()

    conn.row_factory = old_factory
    
    return concepts


</t>
<t tx="karstenw.20230503212558.1">def getedges( conn, conceptid, relationIDs=False, maxedges=0, weight=0.0 ):
    """Query the edges for conceptID.
    
    Currently only queries the left entry / concept1, TODO
    
    Currently ignores the relationIDs parameter, which soulb be a list of relations.
    
    """

    # fetch relations
    query = (
        "SELECT concept1id,relationid,concept2id,weight "
        "FROM edge "
        "WHERE concept1id=%i "
        "AND weight&gt;=%f "
        "ORDER BY weight DESC " )

    query = query % ( conceptid, weight)

    # maxedges return 
    m = 0
    try:
        m = int(maxedges)
    except:
        pass
    if m:
        query = query + " LIMIT %i" % (m,)

    cursor = executeQuery(conn, query )
    edges = cursor.fetchall()

    weightlimit = weight
    result = []
    for edge in edges:
        concept1id,relationid,concept2id,weight = edge

        relation = relations.get( relationid, "" )
        relationname = relation.get( 'patternrelation', "" )
        reverse = relation.get( 'reverse', 0 )
        symmetric = relation.get( 'symmetric', 0 )

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
    
    old_factory = conn.row_factory
    conn.row_factory = dict_factory

    # pdb.set_trace()

    query = ("SELECT idconcept,languagecode,concept,typ,context "
             "FROM concept "
             "WHERE idconcept=? " )

    searchvalues = [conceptid,]

    cursor = executeQuery(conn, query, searchvalues )
    concepts = cursor.fetchall()
    result = {}
    if concepts:
        result = concepts[0]
    conn.row_factory = old_factory
    
    return result


</t>
<t tx="karstenw.20230511095450.1">@language python
@tabwidth -4
@others
if 1: # __name__ == '__main__':
    print()
    handleDataArchive( ZIPARCHIVE, basefolder )
    print()
    importConceptnetTables(conceptsdump, edgesdump)


</t>
<t tx="karstenw.20230511095516.1">

import sys
import os
import io
import time

import zipfile


import pdb
import pprint
pp=pprint.pprint

try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

print("PACKAGE_DIR:", PACKAGE_DIR)

PARENT_DIR, _ = os.path.split( PACKAGE_DIR )
print("PARENT_DIR:", PARENT_DIR)
sys.path.insert(0, PARENT_DIR)


import sdb
getconnection = sdb.getconnection
createRecord = sdb.createRecord
commit = sdb.commit
dotprinter = sdb.dotprinter
tabline2items = sdb.tabline2items
getTableFieldnames = sdb.getTableFieldnames


</t>
<t tx="karstenw.20230511095516.2">def importConceptnetTables( conceptpath, edgepath):
    total = time.time()    
    # side effect - create sqlite database and fill it with the contant tables (language, relation, context)
    conn = getconnection( databasefile )

    bucketsize = 50000

    def emptyBucket(conn, bucket, tablename):
        c = conn.cursor()
        insert = 'INSERT INTO "%s" VALUES (?,?,?,?,?);' % (tablename,)
        c.executemany( insert, bucket )
        commit( conn )

    bucket = []
    
    # pdb.set_trace()
    
    for name in (conceptpath, edgepath):
        start = time.time()
        i = 0
        folder, filename = os.path.split( name )
        tablename, _ = os.path.splitext( filename )
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

        "CREATE INDEX idx_idedge  on edge (idedge);",
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
<t tx="karstenw.20230511095550.1">
DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )


ZIPARCHIVE = os.path.join( PACKAGE_DIR, "conceptnetreader/data/data.zip" )

basefolder = os.path.join( DATA_DIR, "conceptnet-data" )
if not os.path.exists( basefolder ):
    os.makedirs( basefolder )

conceptsdump = os.path.join( basefolder, "concept.tab" )
edgesdump = os.path.join( basefolder, "edge.tab" )
databasefile =  os.path.join( basefolder, "conceptnet.sqlite3" )
if 1:
    print("conceptsdump:", conceptsdump )
    print("edgesdump:", edgesdump )
    print("databasefile:", databasefile )


exportfoldersqlite = os.path.join( basefolder, "sqliteimport")
exportfolderfilemaker = os.path.join( basefolder, "fmpimport")

</t>
<t tx="karstenw.20230511100003.1">def handleDataArchive( zipfilepath, extractdir ):
    """
    """
    with zipfile.ZipFile( zipfilepath ) as archivezip:
        zipmembers = archivezip.infolist()
        for zipmember in zipmembers:
            filename = zipmember.filename
            if filename.startswith('_'):
                print("SKIPPED ZIFILEMEMBER:", filename)
                continue
            basename, ext = os.path.splitext( filename )
            if ext not in (".tab", ".sqlite3"):
                print("SKIPPED:", filename)
                continue
            zipmember.filename = zipmember.filename.replace( "data/", "")
            print("EXTRACT zipfilename:", zipmember.filename )
            archivezip.extract( zipmember, extractdir )
    print("EXTRACT DONE!")


</t>
<t tx="karstenw.20230511121040.1">def readstatic( path ):
    """read a tabtext export.
    
    Yield per record
    """
    
    f = io.open(path, 'r', encoding="utf-8")
    i = 0
    for line in f:
        items = tabline2items( line )
        yield items
        i += 1
    return i

</t>
</tnodes>
</leo_file>
