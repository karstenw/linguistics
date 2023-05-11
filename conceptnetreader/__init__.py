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



analyzed = False

PACKAGE_DIR, _ = os.path.split( os.path.abspath( __file__ ) )
DATA_DIR = os.path.abspath( os.path.join( PACKAGE_DIR, '..', '..', 'linguistics-data', 'conceptnet-data' ) )

databasefile = os.path.abspath("./data/conceptnet.sqlite3")

languages = relations = contexts = ""

inited = False

def initlib():
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


database = {
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


def getconcept( conn, concept, context, lang, relation, slack=False ):

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


def getconceptByID( conn, conceptid ):
    
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


def getedges( conn, conceptid, relationIDs=False, maxedges=0, weight=0.0 ):
    """Query the edges for conceptID.
    
    Currently only queries the left entry / concept1, TODO
    
    Currently ignores the relationIDs parameter, which soulb be a list of relations.
    
    """

    # fetch relations
    query = (
        "SELECT concept1id,relationid,concept2id,weight "
        "FROM edge "
        "WHERE concept1id=%i "
        "AND weight>=%f "
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


def query_concept( concept, relation=None, context=None, maxedges=None, lang="en", weight=0.0 ):
    """Retrieve a concept from the sqlite database.
    
    relation & context are ignored in getedges.
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


if __name__ == "__main__":
    pass


