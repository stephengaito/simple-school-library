
from schoolLib.tools.dbUpdates.utils import addDbVersion, createATable, \
  reCreateIndex, reCreateItemsFTS, reCreateBorrowersFTS

def update(db) :

  print("  Creating initial database ")
  createATable(db, 'classes')
  createATable(db, 'borrowers')
  createATable(db, 'itemsInfo')
  createATable(db, 'itemsPhysical')
  createATable(db, 'itemsBorrowed')
  createATable(db, 'itemsReturned')

  reCreateIndex(db, 'isbn', 'itemsInfo', 'isbn')
  reCreateIndex(db, 'barcode', 'itemsPhysical', 'barCode')
  reCreateBorrowersFTS(db)
  reCreateItemsFTS(db)

addDbVersion('v00000000', update)
