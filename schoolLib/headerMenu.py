

from schoolLib.setup import *
from schoolLib.htmxComponents import *

# dynamic dispatch: use
#  globals()[aStr]
#  locals()[aStr]
#  getattr(aModule, aString)

from schoolLib.setup import *

topLevelMenu = [
  { 'component' : 'button',
    'text' : 'Home',
    'get' : '/menu/home',
  },
  { 'component' : 'button',
    'text' : 'Books',
    'get' : "/menu/books",
  },
  { 'component' : 'button',
    'text' : 'People',
    'get' : '/menu/people'
  },
  { 'component' : 'button',
    'text' : 'Tasks',
    'get' : '/menu/tasks'
  }
]

@get('/headerMenu/{menuPath:path}')
def headerMenu(request, menuPath=None) :
  if menuPath :
    print(f"headerMenu : [{menuPath}] ({type(menuPath)})")
  return GotoResponse('/')

if __name__ == '__main__' :
  print(menu(
    topLevelMenu, theId='silly', get='/homePage'
  ))