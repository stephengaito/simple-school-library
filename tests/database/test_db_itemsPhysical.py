
##############################################
# We need to test the following pageParts:
#
#  app.books.itemsPhysical.postSaveNewItemsPhysical (DONE)
#    InsertSql, SelectSql
#      , 'itemsPhysical', 'itemsInfo', 'itemsFTS'
#
#  app.books.itemsPhysical.getEditItemsPhysicalForm
#    SelectSql
#      , 'itemsPhysical'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsPhysical.putUpdateAnItemsPhysical (DONE)
#    InsertSql, SelectSql, UpdateSql
#      , 'itemsPhysical', 'itemsInfo', 'itemsFTS'

import yaml

import schoolLib

from schoolLib.setup.database import SelectSql

from tests.utils.utils import getMockPageDataFrom, \
  structureHasKeyValue

def test_addSomeItemsPhysical(
  database, addSomeItemsInfo, addSomeItemsPhysical
) :
  selectSql = SelectSql(
  ).fields(
    'itemsInfoId',
    'barCode', 'dateAdded', 'dateBorrowed', 'dateLastSeen',
    'notes', 'status', 'location'
  ).tables(
    'itemsPhysical'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[0], "barCode", "2025-0001")
  assert structureHasKeyValue(results[0], "dateAdded", "2025-03-10")

  assert structureHasKeyValue(results[1], "barCode", "2025-0002")
  assert structureHasKeyValue(results[1], "dateAdded", "2025-03-20")

  assert structureHasKeyValue(results[2], "barCode", "2025-0003")
  assert structureHasKeyValue(results[2], "dateAdded", "2025-03-21")

  selectItemsFTSSql = SelectSql(
  ).fields(
    'itemsInfoId', 'title', 'authors'
  ).tables('itemsFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'itemsFTS', 'Heb*', operator='MATCH'
  )
  results = selectItemsFTSSql.parseResults(
    database.execute(selectItemsFTSSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 1

  assert structureHasKeyValue(results[0], "authors", "Hebditch, Felicity")
  assert structureHasKeyValue(results[0], "title", "Roman Britain")
  assert structureHasKeyValue(results[0], "itemsInfoId", "1")

def test_postSaveNewItemsPhysical(
  database, addSomeItemsInfo, addSomeItemsPhysical
) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      barcode: ''
      dateAdded: '2025-03-30'
      dateBorrowed: '2025-03-30'
      dateLastSeen: '2025-03-30'
      status: ''
  """)

  selectSql = SelectSql(
  ).fields(
    'itemsInfoId',
    'barCode', 'dateAdded', 'dateBorrowed', 'dateLastSeen',
    'notes', 'status', 'location'
  ).tables(
    'itemsPhysical'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[0], "barCode", "2025-0001")
  assert structureHasKeyValue(results[0], "dateAdded", "2025-03-10")

  assert structureHasKeyValue(results[1], "barCode", "2025-0002")
  assert structureHasKeyValue(results[1], "dateAdded", "2025-03-20")

  assert structureHasKeyValue(results[2], "barCode", "2025-0003")
  assert structureHasKeyValue(results[2], "dateAdded", "2025-03-21")

  schoolLib.app.books.itemsPhysical.postSaveNewItemsPhysical(
    pageData, itemsInfoId=3
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 4

  assert structureHasKeyValue(results[3], "barCode", "2025-0004")
  assert structureHasKeyValue(results[3], "dateAdded", "2025-03-30")

  selectItemsFTSSql = SelectSql(
  ).fields(
    'itemsInfoId', 'title', 'authors'
  ).tables('itemsFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'itemsFTS', 'Heb*', operator='MATCH'
  )
  results = selectItemsFTSSql.parseResults(
    database.execute(selectItemsFTSSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 1

  assert structureHasKeyValue(results[0], "authors", "Hebditch, Felicity")
  assert structureHasKeyValue(results[0], "title", "Roman Britain")
  assert structureHasKeyValue(results[0], "itemsInfoId", "1")


def test_putUpdateAnItemsPhysical(
  database, addSomeItemsInfo, addSomeItemsPhysical
) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      barcode: '2025-0002'
      dateAdded: '2025-03-30'
      dateBorrowed: '2025-03-30'
      dateLastSeen: '2025-03-30'
      status: ''
  """)

  selectSql = SelectSql(
  ).fields(
    'itemsInfoId',
    'barCode', 'dateAdded', 'dateBorrowed', 'dateLastSeen',
    'notes', 'status', 'location'
  ).tables(
    'itemsPhysical'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[0], "barCode", "2025-0001")
  assert structureHasKeyValue(results[0], "dateAdded", "2025-03-10")

  assert structureHasKeyValue(results[1], "barCode", "2025-0002")
  assert structureHasKeyValue(results[1], "dateAdded", "2025-03-20")

  assert structureHasKeyValue(results[2], "barCode", "2025-0003")
  assert structureHasKeyValue(results[2], "dateAdded", "2025-03-21")

  schoolLib.app.books.itemsPhysical.putUpdateAnItemsPhysical(
    pageData, itemsPhysicalId=2
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[1], "barCode", "2025-0002")
  assert structureHasKeyValue(results[1], "dateAdded", "2025-03-30")

  selectItemsFTSSql = SelectSql(
  ).fields(
    'itemsInfoId', 'title', 'authors'
  ).tables('itemsFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'itemsFTS', 'Heb*', operator='MATCH'
  )
  results = selectItemsFTSSql.parseResults(
    database.execute(selectItemsFTSSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 1

  assert structureHasKeyValue(results[0], "authors", "Hebditch, Felicity")
  assert structureHasKeyValue(results[0], "title", "Roman Britain")
  assert structureHasKeyValue(results[0], "itemsInfoId", "1")

  # assert False

