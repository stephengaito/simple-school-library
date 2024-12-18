
# import sqlite3
import yaml

from schoolLib.setup.database import SelectSql
#  InsertSql, getClasses, getSortedClasses

# from schoolLib.tools.dbUpdates.utils import CreateSql

from tests.utils.utils import structureHasKeyValue

def test_classesAdded(database, addSomeClasses) :
  """ Test to ensure that the addSomeClasses fixture has added the
  expected classes """

  selectSql = SelectSql(
  ).fields("id", "name", "classOrder", "desc", "colour"
  ).tables("classes"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert structureHasKeyValue(results, "name", "Badgers")
  assert structureHasKeyValue(results, "desc", "The owls")
  assert structureHasKeyValue(results, "colour", "orange")
  assert structureHasKeyValue(results, "classOrder", 20)

"""
def test_getDatabase() :
  results = []
  # we set the path explicitly so we do not use a local database.
  with sqlite3.connect(':memory:') as db :
    db.execute(CreateSql().sql("borrowers"))
    db.execute(*InsertSql().sql('borrowers', {
      "firstName" : 'Stephen',
      "familyName" : 'Gaito'
    }))
    db.commit()
    selectSql = SelectSql(
    ).fields("firstName", "familyName"
    ).tables('borrowers')
    results = selectSql.parseResults(
      db.execute(selectSql.sql())
    )
  print(yaml.dump(results))
  assert len(results) == 1
  assert isinstance(results[0], dict)
  assert 'firstName'  in results[0]
  assert 'familyName' in results[0]
  assert results[0]['firstName']  == 'Stephen'
  assert results[0]['familyName'] == 'Gaito'

def test_classes() :
  theClasses = {}
  sortedClasses = []
  # we set the path explicitly so we do not use a local database.
  with sqlite3.connect(':memory:') as db :
    db.execute(CreateSql().sql('classes'))
    db.execute(*InsertSql().sql('classes', {
      'name' : 'Oak class',
      'classOrder' : 10,
      'desc' : '',
      'colour' : '#000000'
    }))
    db.execute(*InsertSql().sql('classes', {
      'name' : 'Wise class',
      'classOrder' : 1,
      'desc' : '',
      'colour' : '#000000'
    }))
    db.commit()
    theClasses = getClasses(db, selectedClass=2)
    sortedClasses = getSortedClasses(theClasses)
  print(yaml.dump(theClasses))
  print(yaml.dump(sortedClasses))

  assert isinstance(theClasses, dict)
  assert isinstance(sortedClasses, list)

  assert 0 not in theClasses
  assert 1     in theClasses
  assert 2     in theClasses
  assert 3 not in theClasses
  assert len(theClasses) == 2

  assert 'classOrder' in theClasses[2]
  assert 'name'       in theClasses[2]
  assert 'desc'       in theClasses[2]
  assert 'colour'     in theClasses[2]
  assert 'selected'   in theClasses[2]
  assert theClasses[2]['selected'] == 'selected'
  assert theClasses[2]['name']     == 'Wise class'

  assert 'selected'   in theClasses[1]
  assert theClasses[1]['selected'] == ''

  assert len(sortedClasses) == 2
  assert sortedClasses[0]['classOrder'] == theClasses[2]['classOrder']
  assert sortedClasses[1]['classOrder'] == theClasses[1]['classOrder']
  assert sortedClasses[0]['name']       == theClasses[2]['name']
  assert sortedClasses[1]['name']       == theClasses[1]['name']
"""
