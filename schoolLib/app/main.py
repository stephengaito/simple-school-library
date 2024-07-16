
import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *
from schoolLib.htmxComponents import *

loadedConfig('config.yaml', verbose=True)
loadedTheme()

# The ORDER here is important!
import schoolLib.app.home.menu
import schoolLib.app.books
import schoolLib.app.people
import schoolLib.app.tasks.menu

@get('/')
def homepage(request):
  return HTMXResponse(
    request,
    htmlPage(
      stdHeaders(),
      stdBody()
    )
  )

@get('/help/{aPath:path}')
def helpPages(request, aPath=None) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='home'),
      level1div(markdownDiv(someMarkdown))
    ])
  )

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='home'),
      level1div([
        text("Opps! Something went wrong! We can't find that page!", type='p'),
        text(f"Looking for: [{request.url}]", type='p')
      ])
    ]),
    status_code=404
  )

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='home'),
      level1div([
        text("Opps! Something went wrong! We can't find that page!", type='p'),
        text(f"Looking for: [{request.url}]", type='p'),
        text(f"Error: {repr(theException)}", type="p"),
      ])
    ]),
    status_code=500
  )

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  }
)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

#for aRoute in routes :
#  print(aRoute.path)
#  print(aRoute.methods)
#  print(aRoute.endpoint)
#  print("")
