
# We need to be VERY careful with ANY imports
from schoolLib.setup.router   import pagePart
from schoolLib.htmxComponents import *

@pagePart
def topLevelMenu(pageData, selectedId=None, **kwargs) :
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
