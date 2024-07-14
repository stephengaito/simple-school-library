
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
  return MarkdownResponse(request, aPath)

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return TemplateResponse(request, "404.html", status_code=404)

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return TemplateResponse(request, "500.html", status_code=500)

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
