import yaml

import schoolLib

from schoolLib.setup.database import SelectSql, \
  getClasses

from tests.utils.utils import structureHasKeyValue, \
  getMockPageDataFrom

##############################################
# We need to test the following methods:
#
#  getClasses           (DONE)
#  getSortedClasses     (ignore for now)
#  getOrderedClassList  (ignore for now)
#
# We need to test the following pageParts:
#
#  app.people.classes.listClasses
#    (getClasses, getSortedClasses)
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.people.classes.postSaveNewClass  (DONE)
#    InsertSql
#      'classes',
#
#  app.people.classes.putUpdateAClass   (DONE)
#    UpdateSql
#      'classes',

def test_addSomeClasses(database, addSomeClasses) :
  """ Test to ensure that the addSomeClasses fixture has added the
  expected classes."""

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

def test_getClasses(database, addSomeClasses) :
  """ Test to ensure that the getClasses method returns the expected
  classes."""

  theClasses = getClasses(database, selectedClass=1)
  assert len(theClasses) == 3
  for aKey, aValue in theClasses.items() :
    assert 'classOrder' in aValue
    assert 'colour' in aValue
    assert 'desc' in aValue
    assert 'id' in aValue and aValue['id'] == aKey
    assert 'name' in aValue
    assert 'selected' in aValue

  assert theClasses[1]['selected'] == 'selected'
  assert theClasses[2]['name'] == 'Squirrels'
  assert theClasses[3]['colour'] == 'purple'
  assert theClasses[1]['classOrder'] == 10

def test_postSaveNewClass(database, addSomeClasses) :
  """ Test to ennsure the postSaveNewClass makes the correct changes to
  the database."""

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      className:   Rabbits
      classOrder:  30
      classDesc:   The rabbits
      classColour: blue
  """)
  schoolLib.app.people.classes.postSaveNewClass(pageData)
  theClasses = getClasses(database)
  assert len(theClasses) == 4

  # no change to existing data
  assert theClasses[1]['selected'] == ''
  assert theClasses[2]['name'] == 'Squirrels'
  assert theClasses[3]['colour'] == 'purple'
  assert theClasses[1]['classOrder'] == 10

  # check for new data
  assert theClasses[4]['name']        == 'Rabbits'
  assert theClasses[4]['classOrder']  == 30
  assert theClasses[4]['desc']        == 'The rabbits'
  assert theClasses[4]['colour']      == 'blue'

def test_putUpdateAClass(database, addSomeClasses) :
  """ Test to ensure the putUpdateAClass method make the correct changes
  to the database."""

  # check before the update
  theClasses = getClasses(database)
  assert len(theClasses) == 3
  assert theClasses[2]['name']        == 'Squirrels'
  assert theClasses[2]['classOrder']  == 20
  assert theClasses[2]['desc']        == 'The squirrels'
  assert theClasses[2]['colour']      == 'orange'

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      className:   Rabbits
      classOrder:  '30'
      classDesc:   The rabbits
      classColour: blue
  """)
  schoolLib.app.people.classes.putUpdateAClass(pageData, classId=2)

  # check after the update
  theClasses = getClasses(database)
  assert len(theClasses) == 3
  assert theClasses[2]['name']        == 'Rabbits'
  assert theClasses[2]['classOrder']  == 30
  assert theClasses[2]['desc']        == 'The rabbits'
  assert theClasses[2]['colour']      == 'blue'

