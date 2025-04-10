##############################################
# We need to test the following pageParts:
#
#  app.people.classesBorrowers.listPupilsInAClassTable  (DONE)
#    SelectSql
#      "classes", "borrowers"
#
#  app.people.classesBorrowers.updatePupilsInClassForm  (DONE)
#    SelectSql
#      "classes", "borrowers"
#
#  app.people.borrowers.editBorrowerForm                (DONE)
#    SelectSql
#      'borrowers'

# import yaml

import schoolLib

from schoolLib.htmxComponents import RefreshMainContent, \
  Table, TableRow, Text, Button, FormTable, ClassesSelector, \
  TextInput, NumberInput

from tests.utils.utils import MockPageData

def test_listPupilsInAClassTable(
  database, addSomeClasses, addSomeBorrowers
) :
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.people.classesBorrowers.listPupilsInAClassTable(
    pageData, classId=2
  )
  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 1
  htmxTable = htmx.content[0]
  assert htmxTable.isA(Table)
  assert len(htmxTable.children) == 3
  aRow = htmxTable.children[2]
  assert aRow.isA(TableRow)
  assert len(aRow.children) == 5

  assert aRow.children[0].component.isA(Text)
  assert aRow.children[0].component.children[0] == 'Folk'

  assert aRow.children[1].component.isA(Text)
  assert aRow.children[1].component.children[0] == 'Curtain'

  assert aRow.children[2].component.isA(Text)
  assert aRow.children[2].component.children[0] == '2023'

  assert aRow.children[3].component.isA(Text)
  assert 'Squirrels' in aRow.children[3].component.children[0]

  assert aRow.children[4].component.isA(Button)
  assert aRow.children[4].component.children[0] == 'Edit'
  assert aRow.children[4].component.hxGet == '/borrowers/edit/3'

def test_updatePupilsInClassForm(
  database, addSomeClasses, addSomeBorrowers
) :
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.people.classesBorrowers.updatePupilsInClassForm(
    pageData, classId=2, hxPost='/'
  )
  assert htmx.isA(FormTable)
  htmxFormTable = htmx
  assert len(htmxFormTable.children) == 1
  aFormTable = htmxFormTable.children[0]
  assert aFormTable.isA(Table)
  assert len(aFormTable.children) == 3
  aRow = aFormTable.children[2]
  assert aRow.isA(TableRow)
  assert len(aRow.children) == 5

  assert aRow.children[0].component.isA(Text)
  assert aRow.children[0].component.children[0] == 'Folk'

  assert aRow.children[1].component.isA(Text)
  assert aRow.children[1].component.children[0] == 'Curtain'

  assert aRow.children[2].component.isA(Text)
  assert aRow.children[2].component.children[0] == '2023'

  assert aRow.children[3].component.isA(Text)
  assert 'Squirrels' in aRow.children[3].component.children[0]

  assert aRow.children[4].component.isA(ClassesSelector)
  assert aRow.children[4].component.name == 'rowClass-3'

def test_editBorrowerForm(
  database, addSomeClasses, addSomeBorrowers
) :
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.people.borrowers.editBorrowerForm(
    pageData, 2, hxPost='/'
  )
  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 1
  htmxFormTable = htmx.content[0]
  assert htmxFormTable.isA(FormTable)
  assert len(htmxFormTable.children) == 1
  aTable = htmxFormTable.children[0]
  assert aTable.isA(Table)
  assert len(aTable.children) == 4

  assert aTable.children[0].isA(TextInput)
  assert aTable.children[0].name == "firstname"

  assert aTable.children[1].isA(TextInput)
  assert aTable.children[1].name == "familyName"

  assert aTable.children[2].isA(NumberInput)
  assert aTable.children[2].name == "cohort"

  assert aTable.children[3].isA(ClassesSelector)
  assert aTable.children[3].name == "assignedClass"

