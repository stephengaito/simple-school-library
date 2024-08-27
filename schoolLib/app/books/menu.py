

from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelBooksMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'Take a book out of the library',
      theId    = 'takeOut',
      hxGet    = '/menu/books/takeOut',
      hxTarget = '#level1div'
    ),
    Button(
      'Return books to the library',
      theId    = 'return',
      hxGet    = '/menu/books/return',
      hxTarget = '#level1div'
    ),
    Button(
      'Find a book',
      theId    = 'findBook',
      hxGet    = '/search/items',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendAChild(
      Button(
        'Add a book',
        theId    = 'addBook',
        hxGet    = '/itemsInfo/new',
        hxTarget = '#level1div'
      )
    )
  return theMenu

@pagePart
def secondLevelSingleBookMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([], klassName='vertical')

  # edit itemInfo
  # delete book (only if no copies)
  # add a copy

  if pageData.user.is_authenticated :
    pass

  if selectedId : theMenu.select(selectedId)
  return theMenu

@pagePart
def booksMenu(pageData, **kwargs) :

  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    Level1div([
      secondLevelBooksMenu(pageData),
      getHelpPage(
        pageData, 'booksPage', modal=False,
        hxPost='/editHelp/booksPage/nonModal'
      )
    ])
  ])

##########################################################################
# routes

getRoute('/menu/books', booksMenu, anyUser=True)

@pagePart
def getTakeOutABookForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, selectedId='takeOut'
    ),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      theId='level2div', hxPost='/search/borrowers?level=level0div',
      helpName='findBorrower', placeHolder="Type a borrower's name",
      **kwargs
    )
  ])

getRoute('/menu/books/takeOut', getTakeOutABookForm, anyUser=True)
