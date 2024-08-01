

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

##########################################################################
# routes

@pagePart
async def booksMenu(request, db, **kwargs) :
  someMarkdown = "somthing about **books**"

  return Level0div([
    await callPagePart('app.menus.topLevelMenu', request, db, selectedId='books'),
    Level1div([
      await callPagePart('app.menus.secondLevelBooksMenu', request, db, selectedId='takeOut'),
      MarkdownDiv(someMarkdown)
    ])
  ])

getRoute('/menu/books', booksMenu)
