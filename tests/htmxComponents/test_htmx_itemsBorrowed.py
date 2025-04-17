
##############################################
# We need to test the following pageParts:
#
#  app.utils.finders.getReturnABook                  (DONE)
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsBorrowed.getEditItemsBorrowedForm  (DONE)
#    SelectSql
#      'itemsBorrowed'
#    (does not CHANGE database, so NOT TESTED HERE)
#    (need to checn happy and unhappy paths)
#
#  app.tasks.booksCheckedOut.booksCheckedOut         (DONE)
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#

import yaml

# import pytest

import schoolLib

from schoolLib.htmxComponents import Table, FormTable, \
  RefreshMainContent, DateInput, OobCollection, SearchBox, \
  OobTemplate, Div, Menu, TableRow, TableBody, Text, HelpPage

from tests.utils.utils import MockPageData, getMockPageDataFrom

def test_getReturnABook_happy(
  database, addSomeClasses, addSomeBorrowers,
  addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  pageData = MockPageData(database)
  # Note level= and oobLevel= are never used...
  # search= seems to be just passed through...
  htmx = schoolLib.app.utils.finders.getReturnABook(
    pageData, itemsBorrowedId=2, search='silly'
  )

  print(yaml.dump(htmx))
  assert htmx.isA(OobCollection)
  assert len(htmx.children) == 2
  aDiv      = htmx.children[0]
  aTemplate = htmx.children[1]

  assert aDiv.isA(Div)
  assert len(aDiv.children) == 2
  aSearchBox = aDiv.children[0]
  assert aSearchBox.isA(SearchBox)
  assert aSearchBox.hxPost == '/search/barCode/returnBooks'

  aSearchTable = aDiv.children[1]
  assert aSearchTable.isA(Table)
  assert aSearchTable.theId == 'searchResults'

  assert aTemplate.isA(OobTemplate)
  aTableBody = aTemplate.htmxComponent
  assert aTableBody.isA(TableBody)
  assert aTableBody.hxSwapOob == 'beforeend:#booksReturned'
  assert len(aTableBody.children) == 1
  aTableRow = aTableBody.children[0]
  assert aTableRow.isA(TableRow)
  assert len(aTableRow.children) == 4

def test_getReturnABook_unhappy(
  database, addSomeHelpPages, addSomeClasses, addSomeBorrowers,
  addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  # need to add the booksPage help page
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      helpContent: This is the help for the books page
  """)
  schoolLib.htmxComponents.helpPages.postHelpPage(
    pageData, "booksPage", modal=False
  )

  pageData = MockPageData(database)
  # Note level= and oobLevel= are never used...
  # search= seems to be just passed through...
  htmx = schoolLib.app.utils.finders.getReturnABook(
    pageData, itemsBorrowedId=3, search='silly'
  )

  assert htmx.isA(RefreshMainContent)
  assert htmx.mainMenu.isA(Menu)
  assert htmx.subMenu.isA(Menu)
  assert len(htmx.content) == 1
  helpPage = htmx.content[0]
  assert helpPage.isA(HelpPage)
  assert helpPage.helpPagePath == 'booksPage'
  assert helpPage.rawHtml == 'This is the help for the books page'

def test_getEditItemsBorrowedForm_happy(
  database, addSomeClasses, addSomeBorrowers,
  addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.books.itemsBorrowed.getEditItemsBorrowedForm(
    pageData, itemsPhysicalId=1, itemsBorrowedId=1, borrowersId=1
  )

  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 1
  aFormTable = htmx.content[0]
  assert aFormTable.isA(FormTable)
  assert aFormTable.submitButton.children[0] == 'Save changes'
  assert aFormTable.hxPost == '/itemsBorrowed/1/1/edit/1'

  aTable = aFormTable.children[0]
  assert aTable.isA(Table)
  assert len(aTable.children) == 2

  assert aTable.children[0].isA(DateInput)
  assert aTable.children[0].name == 'dateBorrowed'

  assert aTable.children[1].isA(DateInput)
  assert aTable.children[1].name == 'dateDue'

def test_getEditItemsBorrowedForm_unhappy(
  database, addSomeHelpPages, addSomeClasses, addSomeBorrowers,
  addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :

  # need to add the booksPage help page
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      helpContent: This is the help for the books page
  """)
  schoolLib.htmxComponents.helpPages.postHelpPage(
    pageData, "booksPage", modal=False
  )

  # Now start the test....
  pageData = MockPageData(database, authenticated=True)
  htmx = schoolLib.app.books.itemsBorrowed.getEditItemsBorrowedForm(
    pageData, itemsPhysicalId=1, itemsBorrowedId=1, borrowersId=3
  )

  assert htmx.isA(RefreshMainContent)
  assert htmx.mainMenu.isA(Menu)
  assert htmx.subMenu.isA(Menu)
  assert len(htmx.content) == 1
  helpPage = htmx.content[0]
  assert helpPage.isA(HelpPage)
  assert helpPage.helpPagePath == 'booksPage'
  assert helpPage.rawHtml == 'This is the help for the books page'

  aMenu = htmx.mainMenu
  assert aMenu.isA(Menu)
  assert len(aMenu.children) == 5

  assert aMenu.children[0].hxGet == '/menu/home'
  assert aMenu.children[1].hxGet == '/menu/books'
  assert aMenu.children[2].hxGet == '/menu/people'
  assert aMenu.children[3].hxGet == '/menu/tasks'
  assert aMenu.children[4].hxGet == '/menu/admin'


def test_booksCheckedOut(
  database, addSomeClasses, addSomeBorrowers,
  addSomeItemsInfo, addSomeItemsPhysical, addSomeItemsBorrowed
) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.tasks.booksCheckedOut.booksCheckedOut(
    pageData
  )

  assert htmx.isA(RefreshMainContent)
  assert len(htmx.content) == 1
  aTable = htmx.content[0]

  assert aTable.isA(Table)
  assert len(aTable.children) == 3

  assert aTable.children[0].isA(TableRow)
  assert len(aTable.children[0].children) == 8

