

from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelBooksMenu = [
  { 'component' : 'button',
    'text' : 'Take out a book',
    'get'  : '/menu/books/takeOut'
  },
  { 'component' : 'button',
    'text' : 'Return a book',
    'get'  : '/menu/books/return'
  },
  { 'component' : 'button',
    'text' : 'Renew a book',
    'get'  : '/menu/books/renew'
  },
  { 'component' : 'button',
    'text' : 'Find a book',
    'get'  : '/menu/books/find'
  },
]

@get('/menu/books')
def booksMenu(request) :
  someMarkdown = "somthing about **books**"

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected=1),
      level1div([
        menu(secondLevelBooksMenu, selected=0),
        markdownDiv(someMarkdown)
      ])
    ])
  )
