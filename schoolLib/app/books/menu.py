

from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelBooksMenu = [
  { 'component' : 'button',
    'c-name' : 'takeOut',
    'text' : 'Take out a book',
    'get'  : '/menu/books/takeOut'
  },
  { 'component' : 'button',
    'c-name' : 'return',
    'text' : 'Return a book',
    'get'  : '/menu/books/return'
  },
  { 'component' : 'button',
    'c-name' : 'renew',
    'text' : 'Renew a book',
    'get'  : '/menu/books/renew'
  },
  { 'component' : 'button',
    'c-name' : 'find',
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
      htmxMenu(topLevelMenu, selected='books'),
      level1div([
        htmxMenu(secondLevelBooksMenu, selected='takeOut'),
        markdownDiv(someMarkdown)
      ])
    ])
  )
