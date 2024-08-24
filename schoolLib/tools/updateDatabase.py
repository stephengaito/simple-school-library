
import yaml

from schoolLib.setup import *

import schoolLib.tools.dbUpdates
from   schoolLib.tools.dbUpdates.utils import knownDbVersions

def cli() :

  # load the School Library configuration (to get location of database)
  loadedConfig('config.yaml')
  dbPath = config['database']
  db = sqlite3.connect(dbPath)

  # start by ensuring the dbVersion table exists
  db.execute("""
    CREATE TABLE IF NOT EXISTS dbVersions (
      id      INTEGER PRIMARY KEY AUTOINCREMENT,
      version TEXT NOT NULL
    )
  """)

  selectSql = SelectSql(
  ).fields( 'version'
  ).tables('dbVersions'
  ).orderAscBy('id')
  #print(selectSql.sql())
  dbVersions = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in dbVersions :
    aVersion = aRow['version']
    if aVersion in knownDbVersions :
      del knownDbVersions[aVersion]

  sortedDbVersions = sorted(knownDbVersions.keys())
  for anUpdateVersion in sortedDbVersions :
    try :
      print(f"Running update: {anUpdateVersion}")
      knownDbVersions[anUpdateVersion](db)
      db.execute(*InsertSql().sql('dbVersions', {
        'version' : anUpdateVersion
      }))
      db.commit()
    except Exception as err :
      print(f"Could not update database to version {anUpdateVersion}")
      print(repr(err))
      return 1

  return 0