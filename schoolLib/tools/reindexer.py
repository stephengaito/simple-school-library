
from schoolLib.setup import *

loadedConfig('config.yaml', verbose=True)

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)

    print("Indexing ISBN")
    db.execute("DROP INDEX IF EXISTS isbn")
    db.execute("CREATE INDEX IF NOT EXISTS isbn ON itemsInfo ( isbn )")
    db.commit()

    print("Indexing BarCode")
    db.execute("DROP INDEX IF EXISTS barcode")
    db.execute("""
      CREATE INDEX IF NOT EXISTS barCode ON itemsPhysical ( barCode )
    """)
    db.commit()

    print("FTS indexing borrowers")
    db.execute("DROP TABLE IF EXISTS borrowersFTS")
    db.execute("""
      CREATE VIRTUAL TABLE IF NOT EXISTS borrowersFTS
      USING fts5 ( borrowerId, firstName, familyName )
    """)
    db.commit()

    results = db.execute("SELECT id, firstName, familyName FROM borrowers")
    for aRow in results.fetchall() :
      db.execute("""
        INSERT INTO borrowersFTS ( borrowerId, firstName, familyName)
        VALUES ( ?, ?, ? )
      """, aRow)
    db.commit()

    print("FTS indexing items")
    db.execute("DROP TABLE IF EXISTS itemsFTS")
    db.execute("""
      CREATE VIRTUAL TABLE IF NOT EXISTS itemsFTS
      USING fts5 (
        itemsInfoId, title, authors,
        keywords, summary, type,
        publisher, series, barcode
      )
    """)
    db.commit()

    results = db.execute("""
      SELECT
         itemsInfo.id, title, authors,
         keywords, summary, type,
         publisher, series, barcode
      FROM itemsInfo, itemsPhysical
      WHERE itemsInfo.id = itemsPhysical.itemsInfoId
    """)
    for aRow in results.fetchall() :
      db.execute("""
        INSERT INTO itemsFTS (
         itemsInfoId, title, authors,
         keywords, summary, type,
         publisher, series, barcode
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, aRow)
    db.commit()

  except Exception as err :
    print(f"Could not reindex the database {dbPath}")
    print(repr(err))
  finally :
    db.close()