
from schoolLib.setup import  schemaTables, SqlBuilder

knownDbVersions = {}

def addDbVersion(aVersionId, updateFunc) :
  knownDbVersions[aVersionId] = updateFunc

class CreateSql(SqlBuilder) :

  def sql(self, table) :
    if table not in schemaTables :
      print("CAN NOT CREATE a table if it is not in the schema.yaml")
      return

    fieldList = []
    for aField, aType in schemaTables[table].items() :
      aFieldStmt = f"{aField} {aType.upper()}"
      if aField == "id" :
        aFieldStmt += " PRIMARY KEY AUTOINCREMENT"
      fieldList.append(aFieldStmt)

    cmd = "CREATE TABLE IF NOT EXISTS "
    cmd += table
    cmd += " ( "
    cmd += ", ".join(fieldList)
    cmd += " ) "
    return cmd

def createATable(db, tableName) :
  print(f"Creating table {tableName}")
  createSql = CreateSql().sql(tableName)
  if not createSql :
    raise Exception(f"Could not add {tableName} table")
  db.execute(createSql)

def reCreateIndex(db, indexName, tableName, tableFields) :
  print(f"Indexing {indexName}")
  db.execute(f"DROP INDEX IF EXISTS {indexName}")
  db.execute(
    f"CREATE INDEX IF NOT EXISTS {indexName} ON {tableName} ( {tableFields} )"
  )
  db.commit()

def reCreateBorrowersFTS(db) :
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

def reCreateItemsFTS(db) :
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


