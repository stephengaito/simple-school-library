
# We need to be VERY careful with ANY imports
from schoolLib.setup.router   import pagePart
from schoolLib.htmxComponents import *

@pagePart
async def topLevelMenu(request, db, selectedId=None, **kwargs) :
  return Menu([
    Button(
      'Home',
      theId    = 'home',
      hxGet    = '/menu/home',
      hxTarget = '#level0div'
    ),
    Button(
      'Books',
      theId    = 'books',
      hxGet    = '/menu/books',
      hxTarget = '#level0div'
    ),
    Button(
      'People',
      theId    = 'people',
      hxGet    = '/menu/people',
      hxTarget = '#level0div'
    ),
    Button(
      'Tasks',
      theId    = 'tasks',
      hxGet    = '/menu/tasks',
      hxTarget = '#level0div'
    ),
    Button(
      'Admin',
      theId    = 'admin',
      hxGet    = '/menu/admin',
      hxTarget = '#level0div'
    )
  ], selectedId=selectedId)

@pagePart
async def secondLevelBooksMenu(request, db, selectedId=None, **kwargs) :
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

  if request.user.is_authenticated :
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
async def secondLevelPeopleMenu(request, db, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'List classes',
      theId    = 'listClasses',
      hxGet    = '/menu/people/listClasses',
      hxTarget = '#level1div'
    ),
    Button(
      'Find a person',
      theId    = 'findBorrower',
      hxGet    = '/search/borrowers',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

  if request.user.is_authenticated :
    theMenu.appendChild(
      Button(
        'Add a person',
        theId    = 'addBorrower',
        hxGet    = '/menu/people/addBorrower',
        hxTarget = '#level1div'
      )
    )

    theMenu.appendChild(
      Button(
        'Add a class',
        theId    = 'addClass',
        hxGet    = '/menu/people/addClass',
        hxTarget = '#level1div'
      )
    )

  return theMenu

@pagePart
async def secondLevelTasksMenu(request, db, selectedId=None, **kwargs) :
  return Menu([
    Button(
      'Books checked out',
      theId    = 'booksCheckedOut',
      hxGet    = '/menu/tasks/booksCheckedOut',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

@pagePart
async def secondLevelAdminMenu(request, db, selectedId=None, **kwargs) :
  theMenu = Menu([], klassName='vertical')

  if request.user.is_authenticated :
    theMenu.appendChild(
      Button(
        'Logout',
        theId    = 'logout',
        hxGet    = '/logout',
        hxTarget = '#level1div'
      )
    )
    theMenu.select('logout')
  else :
    theMenu.appendChild(
      Button(
        'Login',
        theId    = 'login',
        hxGet    = '/login',
        hxTarget = '#level1div'
      )
    )
    theMenu.select('login')
  return theMenu
