
##############################################
# We need to test the following pageParts:
#
#  app.utils.finders.getReturnABook
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.books.itemsBorrowed.getEditItemsBorrowedForm
#    SelectSql
#      'itemsBorrowed'
#    (does not CHANGE database, so NOT TESTED HERE)
#
#  app.tasks.booksCheckedOut.booksCheckedOut
#    SelectSql
#      'itemsPhysical', 'borrowers', 'itemsBorrowed', 'itemsInfo'
#    (does not CHANGE database, so NOT TESTED HERE)
#

# import yaml

import schoolLib

from schoolLib.htmxComponents import Table, FormTable, \
  TextInput, RefreshMainContent, DateInput

from tests.utils.utils import MockPageData

def test_getReturnABook(
) :

  schoolLib.app.utils.finders.getReturnABook

