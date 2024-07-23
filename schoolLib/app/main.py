
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
def homepage(request):
  return HtmlPage(
    StdHeaders(),
    StdBody()
  ).response()

@get('/routes/{aPath:path}')
def listRoutes(request, aPath=None) :
  if aPath : aPath = '/'+aPath
  routesHtml = []
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    routesHtml.append(
      Text(' '.join([
        str(aRoute.path),
        str(aRoute.methods),
        str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__)
      ])).response())
  return HTMLResponse('\n'.join(sorted(routesHtml)))

@get('/help/{aPath:path}')
def helpPages(request, aPath=None) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(someMarkdown))
  ]).response()

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
  ]).response(status_code=404)

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
  ]).response(status_code=500)

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  }
)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

