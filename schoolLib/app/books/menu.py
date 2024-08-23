

from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelBooksMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'Take out a book',
      theId    = 'takeOut',
      hxGet    = '/menu/books/takeOut',
      hxTarget = '#level1div'
    ),
    Button(
      'Return a book',
      theId    = 'return',
      hxGet    = '/menu/books/return',
      hxTarget = '#level1div'
    ),
    Button(
      'Renew a book',
      theId    = 'renew',
      hxGet    = '/menu/books/renew',
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
    theMenu.appendChild(
      Button(
        'Add a book',
        theId    = 'addBook',
        hxGet    = '/itemsInfo/new',
        hxTarget = '#level1div'
      )
    )
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
