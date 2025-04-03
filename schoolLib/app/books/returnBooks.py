from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import MainContent, \
  Table, TableHead, TableRow, TableHeader, TableBody, SpacedDiv, Text
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def getReturnBooksPage(pageData, **kwargs) :
  return MainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, selectedId='return'
    ),
    [
      schoolLib.app.utils.finders.returnBooksSearch(pageData, **kwargs),
      SpacedDiv([]),
      Table([
        TableHead([
          TableRow([
            TableHeader(Text("Bar Code")),
            TableHeader(Text("Title")),
            TableHeader(Text("First name")),
            TableHeader(Text("Family name"))
          ])
        ]),
        TableBody([], theId='booksReturned')
      ])
    ]
  )

##########################################################################
# routes

getRoute('/menu/books/return', getReturnBooksPage, anyUser=True)
