
# import sqlite3
import yaml

from schoolLib.setup.database import loadSchema, schemaTables

def test_databaseSchema(database) :
  loadSchema()
  print(yaml.dump(schemaTables))
  noProblemsFound = True
  for aTable, aTableDef in schemaTables.items() :
    print(f"Checking {aTable}")
    missingInTable = set(aTableDef.keys())
    results = database.execute(f"PRAGMA table_info('{aTable}')")
    for aRow in results :
      print(aRow)
      colName = aRow[1]
      colType = aRow[2].lower()
      if colName in missingInTable :
        missingInTable.remove(colName)
      if colName not in aTableDef :
        if not aTable.endswith('FTS') :
          print(f"  Not in Schema: {aTable}.{colName}")
          noProblemsFound = False
      elif colType != aTableDef[colName] :
        print(f"  Incorrect type: {aTable}.{colName} ({colType})")
        noProblemsFound = False
    if missingInTable :
      for aColName in sorted(missingInTable) :
        if not aColName.endswith('FTS') :
          print(f"  Should be in table: {aTable}.{aColName}")
          noProblemsFound = False
  assert noProblemsFound

