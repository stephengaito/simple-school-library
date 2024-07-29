

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

##########################################################################
# routes

@pagePart
def booksMenu(request, db) :
  someMarkdown = "somthing about **books**"

  return Level0div([
    TopLevelMenu.select('books'),
    Level1div([
      SecondLevelBooksMenu.select('takeOut'),
      MarkdownDiv(someMarkdown)
    ])
  ])

getRoute('/menu/books', booksMenu)
