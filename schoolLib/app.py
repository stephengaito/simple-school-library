
import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *

loadedConfig('config.yaml')

# The ORDER here is important!
import schoolLib.classes

@get('/')
def homepage(request):
    return TemplateResponse(request, 'homePage.html')

async def notFound(request, theException) :
  print(repr(request))
  print(repr(theException))
  return TemplateResponse(request, "404.html", status_code=404)

async def serverError(request, theException) :
  print(repr(request))
  print(repr(theException))
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
