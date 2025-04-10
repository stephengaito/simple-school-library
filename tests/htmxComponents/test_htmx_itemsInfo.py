##############################################
# We need to test the following pageParts:
#
#  app.books.itemsInfo.getEditAnItemsInfoForm (DONE)
#    SelectSql
#      'itemsInfo',
#

# import yaml

import schoolLib

from schoolLib.htmxComponents import Table, FormTable, \
  TextInput, TextAreaInput

from tests.utils.utils import MockPageData

def test_getEditAnItemsInfoForm(database, addSomeItemsInfo) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.books.itemsInfo.getEditAnItemsInfoForm(
    pageData, itemsInfoId=2
  )

  assert htmx.isA(FormTable)
  assert len(htmx.children) == 1
  htmxTable = htmx.children[0]
  assert htmxTable.isA(Table)
  assert len(htmxTable.children) == 9
  theRows = htmxTable.children

  assert theRows[0].isA(TextInput)
  assert theRows[0].name == 'title'

  assert theRows[1].isA(TextInput)
  assert theRows[1].name == 'authors'

  assert theRows[2].isA(TextInput)
  assert theRows[2].name == 'publisher'

  assert theRows[3].isA(TextInput)
  assert theRows[3].name == 'type'

  assert theRows[4].isA(TextAreaInput)
  assert theRows[4].name == 'keywords'

  assert theRows[5].isA(TextAreaInput)
  assert theRows[5].name == 'summary'

  assert theRows[6].isA(TextInput)
  assert theRows[6].name == 'series'

  assert theRows[7].isA(TextInput)
  assert theRows[7].name == 'dewey'

  assert theRows[8].isA(TextInput)
  assert theRows[8].name == 'isbn'

