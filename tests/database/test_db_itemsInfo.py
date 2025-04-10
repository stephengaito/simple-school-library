##############################################
# We need to test the following pageParts:
#
#  app.books.itemsInfo.postSaveNewItemsInfo   (DONE)
#    InsertSql
#      'itemsInfo',
#
#  app.books.itemsInfo.getEditAnItemsInfoForm
#    SelectSql
#      'itemsInfo',
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsInfo.putUpdateAnItemsInfo   (DONE)
#    UpdateSql
#      'itemsInfo',

import yaml

import schoolLib

from schoolLib.setup.database import SelectSql

# from schoolLib.htmxComponents import RefreshMainContent, \
#   Table, TableRow, Text, Button, FormTable, ClassesSelector, \
#   TextInput, NumberInput

from tests.utils.utils import getMockPageDataFrom, \
  structureHasKeyValue

def test_addSomeItemsInfo(database, addSomeItemsInfo) :
  selectSql = SelectSql(
  ).fields(
    "id", 'title', 'authors', 'publisher',
    'type',  'keywords', 'summary',
    'series', 'dewey', 'isbn'
  ).tables("itemsInfo"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results, "authors", "Hebditch, Felicity")
  assert structureHasKeyValue(results, "title", "Animals on the Farm")
  assert structureHasKeyValue(results, "dewey", '632')
  assert structureHasKeyValue(results, "isbn", '9780237516420')


def test_postSaveNewItemsInfo(
  database, addSomeItemsInfo
) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      title: Plant Science
      authors: Ganeri, Anita
      publisher: Evans
      type: Hardback
      keywords: ;Biology;Nature;Plants;Science;
      summary: A book about plants
      series: Science Questions and Answers
      dewey: '580'
      isbn: '9780237512460'
  """)

  selectSql = SelectSql(
  ).fields(
    "id", 'title', 'authors', 'publisher',
    'type',  'keywords', 'summary',
    'series', 'dewey', 'isbn'
  ).tables("itemsInfo"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results, "authors", "Hebditch, Felicity")
  assert structureHasKeyValue(results, "title", "Animals on the Farm")
  assert structureHasKeyValue(results, "dewey", '632')
  assert structureHasKeyValue(results, "isbn", '9780237516420')

  schoolLib.app.books.itemsInfo.postSaveNewItemsInfo(pageData)

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 4

  assert structureHasKeyValue(results[3], "authors", "Ganeri, Anita")
  assert structureHasKeyValue(results[3], "title", "Plant Science")
  assert structureHasKeyValue(results[3], "dewey", '580')
  assert structureHasKeyValue(results[3], "isbn", '9780237512460')

def test_putUpdateAnItemsInfo(database, addSomeItemsInfo) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      title: Plant Science
      authors: Ganeri, Anita
      publisher: Evans
      type: Hardback
      keywords: ;Biology;Nature;Plants;Science;
      summary: A book about plants
      series: Science Questions and Answers
      dewey: '580'
      isbn: '9780237512460'
  """)

  selectSql = SelectSql(
  ).fields(
    "id", 'title', 'authors', 'publisher',
    'type',  'keywords', 'summary',
    'series', 'dewey', 'isbn'
  ).tables("itemsInfo"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[1], "authors", "Morgan, Sally")
  assert structureHasKeyValue(results[1], "title", "Animals on the Farm")
  assert structureHasKeyValue(results[1], "dewey", '632')
  assert structureHasKeyValue(results[1], "isbn", '9780749633165')

  schoolLib.app.books.itemsInfo.putUpdateAnItemsInfo(
    pageData, itemsInfoId=2
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[1], "authors", "Ganeri, Anita")
  assert structureHasKeyValue(results[1], "title", "Plant Science")
  assert structureHasKeyValue(results[1], "dewey", '580')
  assert structureHasKeyValue(results[1], "isbn", '9780237512460')

