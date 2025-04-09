
##############################################
# We need to test the following pageParts:
#
# app.people.classes.listClasses (DONE)
#  getClasses
#    classes
#

import schoolLib

from schoolLib.htmxComponents import RefreshMainContent, \
  Table, TableRow, Text, Div, Button

from tests.utils.utils import MockPageData

def test_listClasses(database, addSomeClasses) :
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.people.classes.listClasses(pageData)
  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 1
  htmxTable = htmx.content[0]
  assert htmxTable.isA(Table)
  assert len(htmxTable.children) == 4
  aRow = htmxTable.children[2]
  assert aRow.isA(TableRow)
  assert len(aRow.children) == 7

  assert aRow.children[0].component.isA(Text)
  assert aRow.children[0].component.children[0] == 'Squirrels'

  assert aRow.children[6].component.isA(Div)
  aDiv = aRow.children[6].component.children[0]
  assert aDiv.isA(Button)
  assert aDiv.hxGet == "/classes/delete/2"
  assert aDiv.children[0] == "Delete"

