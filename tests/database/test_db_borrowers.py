import yaml

# import pytest

import schoolLib

from schoolLib.setup.database import SelectSql, \
  getClasses

from tests.utils.utils import structureHasKeyValue, \
  getMockPageDataFrom, MockPageData

##############################################
# We need to test the following pageParts:
#
#  app.people.classes.deleteAnEmptyClass   (DONE)
#    DeleteSql, SelectSql
#      'borrowers', 'classes'
#
#  app.people.classesBorrowers.listPupilsInAClassTable
#    SelectSql
#      "classes", "borrowers"
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.people.classesBorrowers.updatePupilsInClassForm
#    SelectSql
#      "classes", "borrowers"
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.people.classesBorrowers.putUpdatePupilsInAClass  (DONE)
#    UpdateSql
#      'borrowers'
#
#  app.people.borrowers.editBorrowerForm
#    SelectSql
#      'borrowers'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.people.borrowers.postSaveNewBorrower  (DONE)
#    InsertSql, SelectSql
#      'borrowers', 'borrowersFTS'
#
#  app.people.borrowers.putUpdatedBorrower   (DONE)
#    UpdateSql
#      'borrowers', 'borrowersFTS'
#

def test_addSomeBorrowers(
  database, addSomeClasses, addSomeBorrowers
) :
  """ Test to ensure that the addSomeBorrowers fixture has added the
  expected borrowers."""

  selectSql = SelectSql(
  ).fields("id", "firstName", "familyName", "cohort", "classId"
  ).tables("borrowers"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))

  assert structureHasKeyValue(results, "firstName", "Bury")
  assert structureHasKeyValue(results, "familyName", "Track")
  assert structureHasKeyValue(results, "cohort", 2025)
  assert structureHasKeyValue(results, "classId", 2)

def test_deleteAnEmptyClass(
  database, addSomeClasses, addSomeBorrowers
) :
  """ Test to ensure that the deleteAnEmptyClass can delete empty classes
  but not classes with borrowers."""

  pageData = MockPageData(database, authenticated=True)

  theClasses = getClasses(database)
  assert len(theClasses) == 3

  # this should NOT delete the class
  schoolLib.app.people.classes.deleteAnEmptyClass(pageData, classId=2)

  theClasses = getClasses(database)
  assert len(theClasses) == 3

  # this should delete the class
  schoolLib.app.people.classes.deleteAnEmptyClass(pageData, classId=3)

  theClasses = getClasses(database)
  assert len(theClasses) == 2
  assert 1 in theClasses
  assert 2 in theClasses
  assert 3 not in theClasses

def test_postSaveNewBorrower(
  database, addSomeClasses, addSomeBorrowers
) :
  """Test the postSaveNewBorrower pagePart to ensure it correctly adds a
  new user."""

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      firstName:     Ward
      familyName:    Tape
      cohort:        '2022'
      assignedClass: '3'
  """)

  # Check the borrowers table before
  selectBorrowersSql = SelectSql(
  ).fields("id", "firstName", "familyName", "cohort", "classId"
  ).tables("borrowers"
  )
  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  assert len(results) == 3

  schoolLib.app.people.borrowers.postSaveNewBorrower(pageData)

  # Check the borrowers table after
  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 4

  assert structureHasKeyValue(results, "firstName", "Bury")
  assert structureHasKeyValue(results, "familyName", "Track")
  assert structureHasKeyValue(results, "cohort", 2025)
  assert structureHasKeyValue(results, "classId", 2)

  assert structureHasKeyValue(results, "firstName", "Ward")
  assert structureHasKeyValue(results, "familyName", "Tape")
  assert structureHasKeyValue(results, "cohort", 2022)
  assert structureHasKeyValue(results, "classId", 3)

  selectBorrowersFTSSql = SelectSql(
  ).fields(
    'borrowerId', 'firstName', 'familyName'
  ).tables('borrowersFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'borrowersFTS', 'Char*', operator='MATCH'
  )
  results = selectBorrowersFTSSql.parseResults(
    database.execute(selectBorrowersFTSSql.sql())
  )
  assert len(results) == 1
  assert structureHasKeyValue(results, "firstName", 'Charter')
  assert structureHasKeyValue(results, "familyName", 'Track')
  assert structureHasKeyValue(results, "borrowerId", '2')

  selectBorrowersFTSSql = SelectSql(
  ).fields(
    'borrowerId', 'firstName', 'familyName'
  ).tables('borrowersFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'borrowersFTS', 'War*', operator='MATCH'
  )
  results = selectBorrowersFTSSql.parseResults(
    database.execute(selectBorrowersFTSSql.sql())
  )
  assert len(results) == 1
  assert structureHasKeyValue(results, "firstName", 'Ward')
  assert structureHasKeyValue(results, "familyName", 'Tape')
  assert structureHasKeyValue(results, "borrowerId", '4')

  print(yaml.dump(results))

def test_putUpdatedBorrower(
  database, addSomeClasses, addSomeBorrowers
) :
  """Test the putUpdatedBorrower pagePart to ensure it correctly updates a
  user."""

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      firstName:     Ward
      familyName:    Tape
      cohort:        '2022'
      assignedClass: '3'
  """)

  # Check the borrowers table before
  selectBorrowersSql = SelectSql(
  ).fields("id", "firstName", "familyName", "cohort", "classId"
  ).tables("borrowers"
  )
  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  assert len(results) == 3
  assert structureHasKeyValue(results[1], "firstName", "Charter")
  assert structureHasKeyValue(results[1], "familyName", "Track")
  assert structureHasKeyValue(results[1], "cohort", 2024)
  assert structureHasKeyValue(results[1], "classId", 2)

  schoolLib.app.people.borrowers.putUpdatedBorrower(pageData, borrowerId=2)

  # Check the borrowers table after
  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3
  assert structureHasKeyValue(results[1], "firstName", "Ward")
  assert structureHasKeyValue(results[1], "familyName", "Tape")
  assert structureHasKeyValue(results[1], "cohort", 2022)
  assert structureHasKeyValue(results[1], "classId", 3)

  selectBorrowersFTSSql = SelectSql(
  ).fields(
    'borrowerId', 'firstName', 'familyName'
  ).tables('borrowersFTS'
  ).limitTo(10
  ).orderAscBy('rank'
  ).whereValue(
    'borrowersFTS', 'War*', operator='MATCH'
  )
  results = selectBorrowersFTSSql.parseResults(
    database.execute(selectBorrowersFTSSql.sql())
  )
  assert len(results) == 1
  assert structureHasKeyValue(results, "firstName", 'Ward')
  assert structureHasKeyValue(results, "familyName", 'Tape')
  assert structureHasKeyValue(results, "borrowerId", 2)

  print(yaml.dump(results))

def test_putUpdatePupilesInAClass(
  database, addSomeClasses, addSomeBorrowers
) :

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      'rowClass-3' : 'rowClass-3-3'
  """)

  selectBorrowersSql = SelectSql(
  ).fields("id", "firstName", "familyName", "cohort", "classId"
  ).tables("borrowers"
  )
  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3
  assert structureHasKeyValue(results[2], "classId", 2)

  schoolLib.app.people.classesBorrowers.putUpdatePupilsInAClass(pageData)

  results = selectBorrowersSql.parseResults(
    database.execute(selectBorrowersSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3
  assert structureHasKeyValue(results[2], "classId", 3)

