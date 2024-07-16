

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@get('/menu/books')
def booksMenu(request) :
  someMarkdown = "somthing about **books**"

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='books'),
      level1div([
        menu(secondLevelBooksMenu, selected='takeOut'),
        markdownDiv(someMarkdown)
      ])
    ])
  )
