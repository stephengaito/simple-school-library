
from schoolLib.setup import *

loadedConfig('config.yaml', verbose=True)

def cli() :
  with getDatabase() as db :

    db.execute("DROP INDEX IF EXISTS isbn")
    db.execute("CREATE INDEX IF NOT EXISTS isbn ON itemsInfo ( isbn )")
    db.commit()

    db.execute("DROP INDEX IF EXISTS barcode")
    db.execute("""
      CREATE INDEX IF NOT EXISTS barCode ON itemsPhysical ( barCode )
    """)
    db.commit()

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

    db.execute("DROP TABLE IF EXISTS itemsFTS")
    db.execute("""
      CREATE VIRTUAL TABLE IF NOT EXISTS itemsFTS
      USING fts5 (
        itemsInfoId, title, authors,
        keywords, summary, type,
        publisher, series
      )
    """)
    db.commit()

    results = db.execute("""
      SELECT
         id, title, authors,
         keywords, summary, type,
         publisher, series
      FROM itemsInfo
    """)
    for aRow in results.fetchall() :
      db.execute("""
        INSERT INTO itemsFTS (
         itemsInfoId, title, authors,
         keywords, summary, type,
         publisher, series
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """, aRow)
    db.commit()
