
from functools import wraps
from inspect import signature, getdoc, getsource
import re
import sqlite3
#import yaml

from starlette.responses import HTMLResponse
from starlette.routing   import Route #, Mount, WebSocketRoute

from schoolLib.setup.configuration import config

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

routes = []

def htmlResponseFromHtmx(htmxComponent) :
  htmlFragments = []

  # alas this is an implicit cicularlity.... we know that "htmxComponent"
  # objects do response to `collectHtml` messages

  htmxComponent.collectHtml(htmlFragments)
  return HTMLResponse(' '.join(htmlFragments), **htmxComponent.kwargs)

async def callWithParameters(request, func) :
  params = {}
  if request.query_params :
    params.update(request.guery_params)
  if request.path_params :
    params.update(request.path_params)
  path = ":memory:"
  if 'database' in config :
    path = config['database']
  try :
    db = sqlite3.connect(path)
    htmxComponent = await func(request, db, **params)
    return htmlResponseFromHtmx(htmxComponent)
  finally :
    db.close()

def getRoute(aRoute, getFunc, name=None) :
  @wraps(getFunc)
  async def getWrapper(request) :
    return await callWithParameters(request, getFunc)
  routes.append(Route(aRoute, getWrapper, name=name, methods=["GET"]))

def putRoute(aRoute, putFunc, name=None) :
  @wraps(putFunc)
  async def putWrapper(request) :
    return await callWithParameters(request, putFunc)
  routes.append(Route(aRoute, putWrapper, name=name, methods=["PUT", "POST"]))

def postRoute(aRoute, postFunc, name=None) :
  @wraps(postFunc)
  async def postWrapper(request) :
    return await callWithParameters(request, postFunc)
  routes.append(Route(aRoute, postWrapper, name=name, methods=["POST"]))

def patchRoute(aRoute, patchFunc, name=None) :
  @wraps(patchFunc)
  async def patchWrapper(request) :
    return await callWithParameters(request, patchFunc)
  routes.append(Route(aRoute, patchWrapper, name=name, methods=["PATCH", "POST"]))

def deleteRoute(aRoute, deleteFunc, name=None) :
  @wraps(deleteFunc)
  def deleteWrapper(request) :
    return callWithParameters(request, deleteFunc)
  routes.append(Route(aRoute, deleteWrapper, name=name, methods=["GET", "DELETE"]))

###############################################################
# Capture the "external facing" page parts

class PagePartMetaData :
  def __init__(self, func=None, hxUrl=None, hxMethod=None, hxTarget=None) :
    self.func     = func
    self.hxUrl    = hxUrl
    self.hxMethod = hxMethod
    self.hxTraget = hxTarget

pageParts = {}

targetRegExp = re.compile("hxTarget\\s*=\\s*'(.*)'")
getRegExp    = re.compile("hxGet\\s*=\\s*'(.*)'")
postRegExp   = re.compile("hxPost\\s*=\\s*'(.*)'")
callPPRegExp = re.compile("callPagePart\\('(.*)'")

metaDataRegExp = re.compile("hxTarget\\s*=\\s*'(.*)'|hxGet\\s*=\\s*'(.*)'|hxPost\\s*=\\s*'(.*)'|callPagePart\\('(.*)'")

class PagePart :
  def __init__(self, func) :
    self.func = func
    self.name = str(func.__module__)+'.'+str(func.__name__)
    pageParts[self.name] = self

  async def collectMetaData(self) :
    self.sig  = str(signature(self.func))
    self.doc  = getdoc(self.func)
    if not self.doc : self.doc = "No doc string"
    src  = getsource(self.func)
    self.src = src
    metaData = []
    for aMatch in metaDataRegExp.finditer(src) :
      metaData.append(aMatch[0])
    self.metaData = metaData

async def callPagePart(aKey, request, db, **kwargs) :
  if aKey not in pageParts :
    raise HTTPException(404, detail=f"Could not call the page part: {aKey} ")
  return await pageParts[aKey](request, db, **kwargs)

def pagePart(func) :
  PagePart(func)  # register this pagePart
  return func
