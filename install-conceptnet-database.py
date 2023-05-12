

import sys
import os
import io
import time

import zipfile
import gzip

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



DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )


ZIPFOLDER = os.path.join( PACKAGE_DIR, "conceptnetreader/data" )
sqlitezifile =  os.path.join( ZIPFOLDER, "conceptnet.sqlite3.zip" )
conceptsdump = os.path.join( ZIPFOLDER, "concept.tab.gz" )
edgesdump = os.path.join( ZIPFOLDER, "edge.tab.gz" )

basefolder = os.path.join( DATA_DIR, "conceptnet-data" )
if not os.path.exists( basefolder ):
    os.makedirs( basefolder )

databasefile =  os.path.join( basefolder, "conceptnet.sqlite3" )
if 1:
    print("conceptsdump:", conceptsdump )
    print("edgesdump:", edgesdump )
    print("databasefile:", databasefile )


exportfoldersqlite = os.path.join( basefolder, "sqliteimport")
exportfolderfilemaker = os.path.join( basefolder, "fmpimport")

def handleDataArchive_OLD( zipfilepath, extractdir ):
    """Obsolete. Switched to single .gz files due to 100MB limit for github."""

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


def handleDataArchive( zipfilepath, extractdir ):
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


def readstatic( path ):
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

def importConceptnetTables( conceptpath, edgepath):
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
        
        # tablename, _ = os.path.splitext( filename )
        tablename = filename.split( '.' )[0]
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



if 1: # __name__ == '__main__':
    print()
    # pdb.set_trace()
    handleDataArchive( sqlitezifile, basefolder )
    print()
    importConceptnetTables(conceptsdump, edgesdump)


