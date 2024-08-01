
from functools import wraps
from inspect import signature, getdoc, getsource
import re
import sqlite3
import yaml

from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from starlette.routing   import Route #, Mount, WebSocketRoute

from schoolLib.setup.configuration import config

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

routes = []

def htmlResponseFromHtmx(htmxComponent, request) :
  htmlFragments = []

  # alas this is an implicit cicularlity.... we know that "htmxComponent"
  # objects do response to `collectHtml` messages

  kwargs = {}
  htmxComponent.collectHtml(htmlFragments)
  kwargs = htmxComponent.kwargs
  url = request.url.path
  if url != '/' and not url.startswith('/routes') \
    and not url.startswith('/pageParts') and 'develop' in config :
    htmlFragments.insert(
      len(htmlFragments)-1,
      f'<a href="/routes{url}" target="_blank"><img src="/static/svg/bootstrap/code-slash.svg" width="32" height="32"></a>'
    )
  print("-------------------------------------------------")
  print('\n'.join(htmlFragments))
  print("-------------------------------------------------")
  return HTMLResponse('\n'.join(htmlFragments), **kwargs)

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
    return htmlResponseFromHtmx(htmxComponent, request)
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

pageParts = {}

# regexp tester: https://pythex.org/
regExps = [
  r"(?P<level>Level.div)",
  r"hxTarget\s*=\s*'(?P<hxTarget>[^\']*)'",
  r"Link\(\s*f?'(?P<link>[^\']*)'",
  r"hxGet\s*=\s*f?'(?P<hxGet>[^\']*)'",
  r"hxPost\s*=\s*'(?P<hxPost>[^\']*)'",
  r"callPagePart\(\s*\'(?P<callPagePart>[^\']*)\'"
]
metaDataRegExp = re.compile('|'.join(regExps))

class PagePart :
  def __init__(self, func) :
    self.users = set()
    self.func  = func
    name       = str(func.__module__)+'.'+str(func.__name__)
    self.name  = name.lstrip('schoolLib.')
    pageParts[self.name] = self

  def addUser(self, aUser) :
    self.users.add(aUser)

  def collectMetaData(self) :
    self.sig  = str(signature(self.func))
    self.doc  = getdoc(self.func)
    if not self.doc : self.doc = "No doc string"
    src  = getsource(self.func)
    metaData = []
    for aMatch in metaDataRegExp.finditer(src) :
      metaData.append(aMatch.groupdict())
    self.metaData = metaData
    self.src = src

async def callPagePart(aKey, request, db, **kwargs) :
  if aKey not in pageParts :
    raise HTTPException(404, detail=f"Could not call the page part: {aKey} ")
  theFunc = pageParts[aKey].func
  return await theFunc(request, db, **kwargs)

def pagePart(func) :
  PagePart(func)  # register this pagePart
  return func

def computePagePartUsers() :

  # compute the users from each route
  for aRoute in routes :
    aPath = aRoute.path
    anEndpoint = str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__)
    anEndpoint = anEndpoint.lstrip('schoolLib.')
    if anEndpoint in pageParts :
      pageParts[anEndpoint].addUser(aPath)

  # ensure all of the meta data has been collected
  # and then add the users from each pagePart
  for pagePartName, pagePart  in pageParts.items() :
    pagePart.collectMetaData()
    for someMetaData in pagePart.metaData :
      if 'callPagePart' in someMetaData and someMetaData['callPagePart'] :
        if someMetaData['callPagePart'] in pageParts :
          pageParts[someMetaData['callPagePart']].addUser(pagePartName)
