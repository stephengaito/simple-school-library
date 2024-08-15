
from functools import wraps
from inspect import signature, getdoc, getsource, iscoroutinefunction
import re
import sqlite3
import yaml

from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from starlette.routing   import Route #, Mount, WebSocketRoute

from schoolLib.setup.configuration   import config
from schoolLib.htmxComponents.layout import *

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

class SSLRoute(Route) :
  def __init__(self, aRoute, aFunc, anyUser=False, **kwargs) :
    self.anyUser = anyUser
    super().__init__(aRoute, aFunc, **kwargs)

routes    = []

def htmlResponseFromHtmx(htmxComponent, request) :
  htmlFragments = []

  # alas this is an implicit cicularlity.... we know that "htmxComponent"
  # objects do response to `collectHtml` messages

  kwargs = {}
  if 'HX-Request' not in request.headers :
    htmxComponent = HtmlPage(
      StdHeaders(),
      htmxComponent
    )
  htmxComponent.collectHtml(htmlFragments)
  kwargs = htmxComponent.kwargs
  url = request.url.path
  if url != '/' and not url.startswith('/routes') \
    and not url.startswith('/pageParts') and 'develop' in config :
    htmlFragments.insert(
      len(htmlFragments)-1,
      f"""
        <div class="m-5 grid grid-cols-10 gap-4 content-start">
        <a href="/routes{url}" target="_blank"><img src="/static/svg/bootstrap/filetype-py.svg" width="24" height="24"></a>
        <a href="/uiOverview" target="_blank"><img src="/static/svg/bootstrap/braces-asterisk.svg" width="24" height="24"></a>
        </div>
      """
    )
  #print("-------------------------------------------------")
  #print('\n'.join(htmlFragments))
  #print("-------------------------------------------------")
  return HTMLResponse('\n'.join(htmlFragments), **kwargs)

loginFunc = None

def registerLoginPage(aLoginFunc) :
  global loginFunc
  loginFunc = aLoginFunc

async def callWithParameters(request, func, anyUser=False) :
  params = {}
  if request.query_params :
    params.update(request.query_params)
  if request.path_params :
    params.update(request.path_params)
  path = ":memory:"
  if 'database' in config :
    path = config['database']
  try :
    db = sqlite3.connect(path)
    #print(yaml.dump(params))
    if anyUser :
      if iscoroutinefunction(func) :
        htmxComponent = await func(request, db, **params)
      else :
        htmxComponent = func(request, db, **params)
    elif loginFunc :
      message = "You must be logged in to access this page"
      if 'develop' in config :
        message += f" ({request.url.path})"
      htmxComponent = await loginFunc(request, db, message=message)
    else :
      raise HTTPException(
        404,
        detail=f"No login page registered while trying to serve {request.url.path}"
      )
    return htmlResponseFromHtmx(htmxComponent, request)
  finally :
    db.close()

def getRoute(aRoute, getFunc, anyUser=False, name=None) :
  @wraps(getFunc)
  async def getWrapper(request) :
    print(f"Any user: {anyUser}")
    return await callWithParameters(request, getFunc, anyUser=anyUser)
  routes.append(SSLRoute(aRoute, getWrapper, name=name, methods=["GET"]))

def putRoute(aRoute, putFunc, anyUser=False, name=None) :
  @wraps(putFunc)
  async def putWrapper(request) :
    return await callWithParameters(request, putFunc, anyUser=anyUser)
  routes.append(SSLRoute(aRoute, putWrapper, name=name, methods=["PUT", "POST"]))

def postRoute(aRoute, postFunc, anyUser=False, name=None) :
  @wraps(postFunc)
  async def postWrapper(request) :
    return await callWithParameters(request, postFunc, anyUser=anyUser)
  routes.append(SSLRoute(aRoute, postWrapper, name=name, methods=["POST"]))

def patchRoute(aRoute, patchFunc, anyUser=False, name=None) :
  @wraps(patchFunc)
  async def patchWrapper(request) :
    return await callWithParameters(request, patchFunc, anyUser=anyUser)
  routes.append(SSLRoute(aRoute, patchWrapper, name=name, methods=["PATCH", "POST"]))

def deleteRoute(aRoute, deleteFunc, anyUser=False, name=None) :
  @wraps(deleteFunc)
  async def deleteWrapper(request) :
    return await callWithParameters(request, deleteFunc, anyUser=anyUser)
  routes.append(SSLRoute(aRoute, deleteWrapper, name=name, methods=["GET", "DELETE"]))

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
    if anEndpoint not in pageParts :
      print(f"Could not find the endpoint {anEndpoint} in {aRoute}")
      continue
    pageParts[anEndpoint].addUser(aPath)

  # ensure all of the meta data has been collected
  # and then add the users from each pagePart
  for pagePartName, pagePart  in pageParts.items() :
    pagePart.collectMetaData()
    for someMetaData in pagePart.metaData :
      if 'callPagePart' in someMetaData and someMetaData['callPagePart'] :
        if someMetaData['callPagePart'] not in pageParts :
          print(f"Could not find page part {someMetaData['callPagePart']} in {pagePartName}")
          continue
        pageParts[someMetaData['callPagePart']].addUser(pagePartName)
