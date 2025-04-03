
# We need to be VERY careful with ANY imports
from schoolLib.setup.router   import pagePart
from schoolLib.htmxComponents import Menu, Button

@pagePart
def topLevelMenu(pageData, selectedId=None, **kwargs) :
  theKlass = []
  if pageData.user.is_authenticated :
    theKlass = ['bg-red-200']
  theMenu = Menu([
    Button(
      'Home',
      theId    = 'home',
      hxGet    = '/menu/home',
      klass    = theKlass
    ),
    Button(
      'Books',
      theId    = 'books',
      hxGet    = '/menu/books',
      klass    = theKlass
    ),
    Button(
      'People',
      theId    = 'people',
      hxGet    = '/menu/people',
      klass    = theKlass
    )
  ])

  if pageData.user.is_authenticated :
    theMenu.appendAChild(
      Button(
        'Tasks',
        theId    = 'tasks',
        hxGet    = '/menu/tasks',
        klass    = theKlass
      )
    )

  theMenu.appendAChild(
    Button(
      'Admin',
      theId    = 'admin',
      hxGet    = '/menu/admin',
      klass    = theKlass
    )
  )

  if selectedId : theMenu.select(selectedId)

  return theMenu
