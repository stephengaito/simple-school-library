from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Level1div, Div, Level2div, EmptyDiv, \
  Table, TableHead, TableRow, TableHeader, TableBody, SpacedDiv, Text
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def getReturnBooksPage(pageData, **kwargs) :
  return Level1div([
    Div([]),  # no menu
    Level2div([
      schoolLib.app.utils.finders.returnBooksSearch(pageData, **kwargs),
    ]),
    EmptyDiv([]),
    SpacedDiv([]),
    EmptyDiv([]),
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
  ])

##########################################################################
# routes

getRoute('/menu/books/return', getReturnBooksPage, anyUser=True)
