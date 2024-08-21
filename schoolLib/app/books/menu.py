

from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

##########################################################################
# routes

@pagePart
def booksMenu(pageData, **kwargs) :
  someMarkdown = "somthing about **books**"

  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    Level1div([
      schoolLib.app.menus.secondLevelBooksMenu(pageData, selectedId='takeOut'),
      MarkdownDiv(someMarkdown)
    ])
  ])

getRoute('/menu/books', booksMenu, anyUser=True)
