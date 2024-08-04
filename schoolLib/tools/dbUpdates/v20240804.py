
from schoolLib.setup import *
from schoolLib.tools.dbUpdates.utils import addDbVersion

def update(db) :

  print("  Adding HelpPages table ")
  createSql = CreateSql().sql('helpPages')
  if not createSql :
    raise Exception("Could not add helpPages table")
  db.execute(createSql)

  print("  Adding shelf to itemsPhysical table")
  sqlCmd = "ALTER TABLE itemsPhysical ADD shelf TEXT DEFAULT ''"
  db.execute(sqlCmd)

addDbVersion('v20240804', update)
