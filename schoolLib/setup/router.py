
from functools import wraps
#import yaml

from starlette.routing import Route #, Mount, WebSocketRoute

from schoolLib.setup.exceptions import SLException
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

routes = []

def callWithParameters(request, func) :
  params = {}
  if request.query_params :
    params.update(request.guery_params)
  if request.path_params :
    params.update(request.path_params)
  #print("-------------------------------------")
  #print(request.url)
  #print(yaml.dump(params))
  #print("-------------------------------------")
  try :
    path = ":memory:"
    if 'database' in config :
      path = config['database']
    try :
      db = sqlite3.connect(path)
      htmxComponent = func(request, db, **params)
      htmlFragments = []
      htmxComponent.collectHtml(htmlFragments)
      return HTMLResponse(' '.join(htmlFragments), **htmxComponent.kwargs)
    finally :
      db.close()
  except SLException as slErr :
    errorText = [
      Text("Opps! Something in the server went wrong! We can't supply that page!", type='p'),
      Text(slErr.slMessage, type='p'),
      Text(slErr.slErrType, type='p'),
    ]
    if slErr.slHelpMsg : errorText.append(Text(slErr.slHelpMsg, type='p'))
    if slErr.slOrigErr : errorText.append(Text(slErr.slOrigErr, type='p'))
    return Level0div([
      TopLevelMenu,
      Level1div(errorText)
    ]).response()

def getRoute(aRoute, getFunc, name=None) :
  def getWrapper(request) :
    return callWithParameters(request, getFunc)
  routes.append(Route(aRoute, getWrapper, name=name, methods=["GET"]))

def putRoute(aRoute, putFunc, name=None) :
  async def putWrapper(request) :
    return await callWithParameters(request, putFunc)
  routes.append(Route(aRoute, putWrapper, name=name, methods=["PUT", "POST"]))

def postRoute(aRoute, postFunc, name=None) :
  async def postWrapper(request) :
    return await callWithParameters(request, postFunc)
  routes.append(Route(aRoute, postWrapper, name=name, methods=["POST"]))

def patchRoute(aRoute, patchFunc, name=None) :
  async def patchWrapper(request) :
    return await callWithParameters(request, patchFunc)
  routes.append(Route(aRoute, patchWrapper, name=name, methods=["PATCH", "POST"]))

def deleteRoute(aRoute, deleteFunc, name=None) :
  def deleteWrapper(request) :
    return callWithParameters(request, deleteFunc)
  routes.append(Route(aRoute, deleteWrapper, name=name, methods=["GET", "DELETE"]))

###############################################################
# Capture the "external facing" page parts

pageParts = []

def pagePart(func) :
  pageParts.append(func)
  return func
