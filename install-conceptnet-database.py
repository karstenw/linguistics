

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

try:
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError as err:
    print(err)
    PACKAGE_DIR = os.path.abspath( './' )

print("PACKAGE_DIR:", PACKAGE_DIR)

PARENT_DIR, _ = os.path.split( PACKAGE_DIR )
print("PARENT_DIR:", PARENT_DIR)
sys.path.insert(0, PARENT_DIR)



DATA_DIR = os.path.join( PARENT_DIR, "linguistics-data" )
if not os.path.exists( DATA_DIR ):
    os.makedirs( DATA_DIR )


ZIPFOLDER = os.path.join( PACKAGE_DIR, "conceptnetreader/data" )
sqlitezifile =  os.path.join( ZIPFOLDER, "conceptnet.sqlite3.zip" )
conceptsdump = os.path.join( ZIPFOLDER, "concept.tab.gz" )
edgesdump1 = os.path.join( ZIPFOLDER, "edge_aa.tab.gz" )
edgesdump2 = os.path.join( ZIPFOLDER, "edge_ab.tab.gz" )
edgesdump3 = os.path.join( ZIPFOLDER, "edge_ac.tab.gz" )

importfiles = (conceptsdump, edgesdump1, edgesdump2, edgesdump3 )

basefolder = os.path.join( DATA_DIR, "conceptnet-data" )
if not os.path.exists( basefolder ):
    os.makedirs( basefolder )

databasefile =  os.path.join( basefolder, "conceptnet.sqlite3" )
if 1:
    print("conceptsdump:", conceptsdump )
    print("edgesdump1:", edgesdump1 )
    print("edgesdump2:", edgesdump2 )
    print("edgesdump3:", edgesdump3 )
    print("importfiles:", importfiles )
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

def importConceptnetTables( importfiles ):
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


def getconnection( filepath ):
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
            debugprint("")
            debugprint( "ERR: " + repr(err) )
            time.sleep( 0.01 )
            i += 1


def dict_factory(cursor, row):
    # from pysqlite code examples
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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


if 1: # __name__ == '__main__':
    print()
    # pdb.set_trace()
    handleDataArchive( sqlitezifile, basefolder )
    print()
    importConceptnetTables( importfiles )


