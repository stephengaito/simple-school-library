
from schoolLib.tools.dbUpdates.utils import addDbVersion, \
  createATable, reCreateIndex

def update(db) :

  print("  Adding HelpPages table ")
  createATable(db, 'helpPages')

  print("  Adding shelf to itemsPhysical table")
  sqlCmd = "ALTER TABLE itemsPhysical ADD shelf TEXT DEFAULT ''"
  db.execute(sqlCmd)

  reCreateIndex(db, 'helpPagesPath', 'helpPages', 'path')

addDbVersion('v20240804', update)
