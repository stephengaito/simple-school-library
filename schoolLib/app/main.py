
import os

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

@get('/')
def homepage(request, db):
  return HtmlPage(
    StdHeaders(),
    StdBody()
  )

@get('/routes/{aPath:path}')
def listRoutes(request, db, aPath=None) :
  if aPath : aPath = '/'+aPath
  routesStrs = []
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    routesStrs.append(
      ' '.join([
        '<p>',
        str(aRoute.path),
        str(aRoute.methods),
        str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__),
        '</p>'
      ]))
  return Text('\n'.join(sorted(routesStrs)))

@get('/pageParts/{aPath:path}')
def listRoutes(request, db, aPath=None) :
  if aPath : aPath = '/'+aPath
  routesStrs = []
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    routesStrs.append(
      ' '.join([
        '<p>',
        str(aRoute.path),
        str(aRoute.methods),
        str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__),
        '</p>'
      ]))
  return Text('\n'.join(sorted(routesStrs)))

@get('/help/{aPath:path}')
def helpPages(request, db, aPath=None) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(someMarkdown))
  ])

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return Level0div([
    TopLevelMenu.select('home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!"),
      Text(f"Looking for: [{request.url}]")
    ])
  ], status_code=404)

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return Level0div([
    TopLevelMenu.select('home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!", type='p'),
      Text(f"Looking for: [{request.url}]", type='p'),
      Text(f"Error: {repr(theException)}", type="p"),
    ])
  ], status_code=500)

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  }
)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

