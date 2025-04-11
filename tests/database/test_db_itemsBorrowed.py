

##############################################
# We need to test the following pageParts:
#
#  app.utils.finders.getReturnABook
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsBorrowed.postSaveNewItemsBorrowed  (DONE)
#    InsertSql
#      'itemsBorrowed'
#
#  app.books.itemsBorrowed.getEditItemsBorrowedForm
#    SelectSql
#      'itemsBorrowed'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsBorrowed.putUpdateAnItemsBorrowed  (DONE)
#    UpdateSql
#      'itemsBorrowed'
#
#  app.tasks.booksCheckedOut.booksCheckedOut
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#

import yaml

import schoolLib

from schoolLib.setup.database import SelectSql

from tests.utils.utils import getMockPageDataFrom, \
  structureHasKeyValue

def test_addSomeItemsBorrowed(
  database, addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  selectSql = SelectSql(
  ).fields(
    'borrowersId', 'itemsPhysicalId',
    'dateBorrowed', 'dateDue'
  ).tables('itemsBorrowed'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 2

  assert structureHasKeyValue(results[0], "borrowersId", 1)
  assert structureHasKeyValue(results[0], "itemsPhysicalId", 1)
  assert structureHasKeyValue(results[0], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[0], "dateDue", "2025-04-18")

  assert structureHasKeyValue(results[1], "borrowersId", 2)
  assert structureHasKeyValue(results[1], "itemsPhysicalId", 2)
  assert structureHasKeyValue(results[1], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[1], "dateDue", "2025-04-18")

def test_postSaveNewItemsBorrowed(
  database, addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
):
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      dateBorrowed: 2025-04-11
      dateDue: 2025-04-18
  """)

  selectSql = SelectSql(
  ).fields(
    'borrowersId', 'itemsPhysicalId',
    'dateBorrowed', 'dateDue'
  ).tables('itemsBorrowed'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 2

  assert structureHasKeyValue(results[0], "borrowersId", 1)
  assert structureHasKeyValue(results[0], "itemsPhysicalId", 1)
  assert structureHasKeyValue(results[0], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[0], "dateDue", "2025-04-18")

  assert structureHasKeyValue(results[1], "borrowersId", 2)
  assert structureHasKeyValue(results[1], "itemsPhysicalId", 2)
  assert structureHasKeyValue(results[1], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[1], "dateDue", "2025-04-18")

  schoolLib.app.books.itemsBorrowed.postSaveNewItemsBorrowed(
    pageData, itemsPhysicalId=3, borrowersId=3
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[2], "borrowersId", 3)
  assert structureHasKeyValue(results[2], "itemsPhysicalId", 3)
  assert structureHasKeyValue(results[2], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[2], "dateDue", "2025-04-18")


def test_putUpdateAnItemsBorrowed(
  database, addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      dateBorrowed: 2025-04-11
      dateDue: 2025-04-28
  """)

  selectSql = SelectSql(
  ).fields(
    'borrowersId', 'itemsPhysicalId',
    'dateBorrowed', 'dateDue'
  ).tables('itemsBorrowed'
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 2

  assert structureHasKeyValue(results[0], "borrowersId", 1)
  assert structureHasKeyValue(results[0], "itemsPhysicalId", 1)
  assert structureHasKeyValue(results[0], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[0], "dateDue", "2025-04-18")

  assert structureHasKeyValue(results[1], "borrowersId", 2)
  assert structureHasKeyValue(results[1], "itemsPhysicalId", 2)
  assert structureHasKeyValue(results[1], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[1], "dateDue", "2025-04-18")

  schoolLib.app.books.itemsBorrowed.putUpdateAnItemsBorrowed(
    pageData, itemsPhysicalId=2, borrowersId=2, itemsBorrowedId=2
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 2

  assert structureHasKeyValue(results[1], "borrowersId", 2)
  assert structureHasKeyValue(results[1], "itemsPhysicalId", 2)
  assert structureHasKeyValue(results[1], "dateBorrowed", "2025-04-11")
  assert structureHasKeyValue(results[1], "dateDue", "2025-04-28")

