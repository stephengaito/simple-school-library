
import os
import yaml

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

loadedConfig('config.yaml', verbose=True)
loadedTheme()

# The ORDER here is important!
import schoolLib.app.home.menu
import schoolLib.app.books
import schoolLib.app.people
import schoolLib.app.tasks.menu

@pagePart
async def homePage(request, db, **kwargs):
  """ The Home Page """
  return HtmlPage(
    StdHeaders(),
    StdBody()
  )

getRoute('/', homePage)

@pagePart
async def helpPages(request, db, aPath=None, **kwargs) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return Level0div([
    callPagePart(topLevelMenu, selectedId='home'),
    Level1div(MarkdownDiv(someMarkdown))
  ])

getRoute('/help/{aPath:path}', helpPages)

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    await callPagePart('app.menus.topLevelMenu', request, None, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!"),
      Text(f"Looking for: [{request.url}]")
    ])
  ], status_code=404), request)

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    await callPagePart('app.menus.topLevelMenu', request, None, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!", type='p'),
      Text(f"Looking for: [{request.url}]", type='p'),
      Text(f"Error: {repr(theException)}", type="p"),
    ])
  ], status_code=500), request)

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  }
)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

