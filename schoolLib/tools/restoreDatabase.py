
import sqlite3

from schoolLib.setup import config, loadedConfig

loadedConfig('config.yaml')

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)
    with open("tmp/helpPages.sql") as sqlFile :
      aStmt = []
      for line in sqlFile :
        line = line.strip()
        aStmt.append(line)
        if ';' in line :
          aStmt = " ".join(aStmt)
          print(aStmt)
          db.execute(aStmt)
          aStmt = []
  except Exception as err :
    print(repr(err))

