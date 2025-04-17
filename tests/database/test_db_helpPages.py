
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
#  'app.home.home.editHelpPage',  # (1)  return HelpEditorModalDialog(
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  'app.home.home.getHomeMenu',  # (1)
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  'app.home.home.helpPages',  # (1)  return getHelpPage(
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  'app.home.home.homePage',  # (1)
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  'app.home.home.postHelpPages',  # (1) return postHelpPage(

def test_addSomeHelpPages(database, addSomeHelpPages) :
  """ Test to ensure that the addSomeHelpPages fixture has added the
  expected help pages."""

  selectSql = SelectSql(
  ).fields("id", "path", "content"
  ).tables("helpPages"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))

  assert len(results) == 2

  assert structureHasKeyValue(results[0], "path", "helpPage1")
  assert structureHasKeyValue(results[0], "content", "This is the help for page 1")  # noqa
  assert structureHasKeyValue(results[1], "path", "helpPage2")
  assert structureHasKeyValue(results[1], "content", "This is the help for page 2")  # noqa

def test_postHelpPage(database, addSomeHelpPages) :
  """ Test to ensure that the postHelpPage method has added the
  expected help pages."""

  selectSql = SelectSql(
  ).fields("id", "path", "content"
  ).tables("helpPages"
  )
  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )

  assert len(results) == 2

  assert structureHasKeyValue(results[0], "path", "helpPage1")
  assert structureHasKeyValue(results[0], "content", "This is the help for page 1")  # noqa
  assert structureHasKeyValue(results[1], "path", "helpPage2")
  assert structureHasKeyValue(results[1], "content", "This is the help for page 2")  # noqa

  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      helpContent: This is the help for page 3
  """)

  schoolLib.app.home.home.postHelpPages(
    pageData, aHelpPage='helpPage3', isModal='no'
  )

  results = selectSql.parseResults(
    database.execute(selectSql.sql())
  )
  print(yaml.dump(results))
  assert len(results) == 3

  assert structureHasKeyValue(results[0], "path", "helpPage1")
  assert structureHasKeyValue(results[0], "content", "This is the help for page 1")  # noqa
  assert structureHasKeyValue(results[1], "path", "helpPage2")
  assert structureHasKeyValue(results[1], "content", "This is the help for page 2")  # noqa
  assert structureHasKeyValue(results[2], "path", "helpPage3")
  assert structureHasKeyValue(results[2], "content", "This is the help for page 3")  # noqa

