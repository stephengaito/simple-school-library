
##############################################
# We need to test the following pageParts:
#
#  app.books.itemsPhysical.getEditItemsPhysicalForm
#    SelectSql
#      'itemsPhysical'
#
#  NEED TO TEST:
#  1 happy path where itemsPhyscial exists           (DONE)
#  2 unhappy path where itemsPhysical does not exist (DONE)

# import yaml

import schoolLib

from schoolLib.htmxComponents import Table, FormTable, \
  TextInput, RefreshMainContent, DateInput

from tests.utils.utils import MockPageData

def test_getEditItemsPhysicalForm_exists(
  database, addSomeItemsInfo, addSomeItemsPhysical
) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.books.itemsPhysical.getEditItemsPhysicalForm(
    pageData, itemsPhysicalId=2
  )

  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 3
  formTable = htmx.content[2]
  assert formTable.isA(FormTable)
  assert len(formTable.children) == 1
  aTable = formTable.children[0]
  assert aTable.isA(Table)
  assert len(aTable.children) == 7
  rows = aTable.children

  assert rows[0].isA(TextInput)
  assert rows[0].name == 'barcode'

  assert rows[1].isA(DateInput)
  assert rows[1].name == 'dateAdded'

  assert rows[2].isA(DateInput)
  assert rows[2].name == 'dateBorrowed'

  assert rows[3].isA(DateInput)
  assert rows[3].name == 'dateLastSeen'

  assert rows[4].isA(TextInput)
  assert rows[4].name == 'status'

  assert rows[5].isA(TextInput)
  assert rows[5].name == 'notes'

  assert rows[6].isA(TextInput)
  assert rows[6].name == 'location'

def test_getEditItemsPhysicalForm_notExists(
  database, addSomeItemsInfo, addSomeItemsPhysical
) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.books.itemsPhysical.getEditItemsPhysicalForm(
    pageData, itemsPhysicalId=20
  )

  formTable = htmx
  # assert htmx.isA(RefreshMainContent)
  # assert len(htmx.content) == 3
  # formTable = htmx.content[2]
  assert formTable.isA(FormTable)
  assert formTable.submitButton.children[0] == 'Add new book'
  assert formTable.hxPost == '/itemsInfo/new'

