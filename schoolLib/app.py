
import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *

loadedConfig('config.yaml', verbose=True)

# The ORDER here is important!
import schoolLib.classes
import schoolLib.classesBorrowers
import schoolLib.borrowers
import schoolLib.itemsInfo
import schoolLib.itemsPhysical
import schoolLib.itemsBorrowed
import schoolLib.headerMenu

@get('/')
def homepage(request):
    return MarkdownResponse(request, 'homePage')

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

for aRoute in routes :
  print(aRoute.path)
  print(aRoute.methods)
  print(aRoute.endpoint)
  print("")
