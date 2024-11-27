
import sqlite3

from schoolLib.setup import loadedConfig, config
from schoolLib.tools.dbUpdates.utils import reCreateIndex, \
  reCreateBorrowersFTS, reCreateItemsFTS

loadedConfig('config.yaml', verbose=True)

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)

    reCreateIndex(db, 'helpPagesPath', 'helpPages', 'path')
    reCreateIndex(db, 'isbn', 'itemsInfo', 'isbn')
    reCreateIndex(db, 'barcode', 'itemsPhysical', 'barCode')
    reCreateBorrowersFTS(db)
    reCreateItemsFTS(db)

  except Exception as err :
    print(f"Could not reindex the database {dbPath}")
    print(repr(err))
  finally :
    db.close()
