
import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *

loadedConfig('config.yaml')

# The ORDER here is important!
import schoolLib.classes
import schoolLib.classesBorrowers

@get('/')
def homepage(request):
    return TemplateResponse(request, 'homePage.html')

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
