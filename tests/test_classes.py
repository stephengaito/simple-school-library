# import sqlite3
import yaml

import schoolLib
from tests.utils.utils import MockPageData

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

def test_listClasses(database, addSomeClasses) :
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.people.classes.listClasses(pageData)
  print(yaml.dump(htmx))
  assert False

