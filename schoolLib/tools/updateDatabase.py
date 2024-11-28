
import sqlite3
# import yaml

from schoolLib.setup import SelectSql, InsertSql

# import schoolLib.tools.dbUpdates
from schoolLib.tools.dbUpdates.utils import knownDbVersions
from schoolLib.tools.utils import getDatabasePath

def updateDatabase(db) :

  # start by ensuring the dbVersion table exists
  db.execute("""
    CREATE TABLE IF NOT EXISTS dbVersions (
      id      INTEGER PRIMARY KEY AUTOINCREMENT,
      version TEXT NOT NULL
    )
  """)

  # remove all update-version which have already been applied
  selectSql = SelectSql(
  ).fields('version'
  ).tables('dbVersions'
  ).orderAscBy('id')
  # print(selectSql.sql())
  dbVersions = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in dbVersions :
    aVersion = aRow['version']
    if aVersion in knownDbVersions :
      del knownDbVersions[aVersion]

  # apply any update-version which have not already been applied
  sortedDbVersions = sorted(knownDbVersions.keys())
  for anUpdateVersion in sortedDbVersions :
    try :
      print(f"\nRunning update: {anUpdateVersion}")
      knownDbVersions[anUpdateVersion](db)
      db.execute(*InsertSql().sql('dbVersions', {
        'version' : anUpdateVersion
      }))
      db.commit()
    except Exception as err :
      print(f"Could not update database to version {anUpdateVersion}")
      print(repr(err))
      return 1

  print("\nAll updates applied")
  return 0

def cli() :

  # load the School Library configuration (to get location of database)
  db = sqlite3.connect(
    getDatabasePath('slUpdateDatabase')
  )
  return updateDatabase(db)
