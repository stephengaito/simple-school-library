
from functools import wraps
from inspect import signature, getdoc, getsource
import re
import sqlite3
# import yaml

from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from starlette.routing   import Route  # , Mount, WebSocketRoute

from starlette_login.utils import login_user, logout_user

from schoolLib.setup.configuration   import config
from schoolLib.setup.authenticate    import OtherUser

# from schoolLib.htmxComponents.layout import *
from schoolLib.htmxComponents import HtmlPage, StdHeaders, StdBody, \
  WarnFooterMessage, Text

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

class SSLRoute(Route) :
  def __init__(self, aRoute, aFunc, anyUser=False, **kwargs) :
    self.anyUser = anyUser
    super().__init__(aRoute, aFunc, **kwargs)

class PageData :
  def __init__(self, db) :
    self.db      = db
    self.login   = None
    self.logout  = False
    self.headers = {}
    self.form    = {}
    self.path    = "/"
    self.user    = OtherUser()

  async def getRequestData(self, request) :
    self.form    = await request.form()
    self.form    = dict(self.form)
    theHeaders = {}
    for aHeader, aValue in request.headers.items() :
      theHeaders[aHeader] = aValue
    self.headers = theHeaders
    self.path    = request.url.path
    self.user    = request.user

  def setUser(self, user) :
    self.login = user
    self.user  = user

  def shouldLogout(self) :
    self.logout = True
    self.user   = OtherUser()

routes    = []

def htmlResponseFromHtmx(htmxComponent, pageData) :
  htmlFragments = []

  # alas this is an implicit cicularlity.... we know that "htmxComponent"
  # objects do response to `collectHtml` messages

  kwargs = {}
  if 'hx-request' in pageData.headers :
    htmxComponent.collectHtml(htmlFragments)
    url = pageData.path
    if url != '/' and not url.startswith('/routes') \
        and not url.startswith('/pageParts') and 'develop' in config :
      htmlFragments.append(f"""
        <div hx-swap-oob="innerHTML:#developerMessages">
          <a href="/routes{url}" target="_blank">/routes{url}</a>
          &nbsp; &nbsp; &nbsp; &nbsp;
          <!-- a href="/uiOverview{url}" target="_blank">/uiOverview{url}</a -->
        </div>
      """)
  else :
    if isinstance(htmxComponent, HtmlPage) :
      htmxComponent.collectHtml(htmlFragments)
    else :
      htmxComponent = HtmlPage(
        StdHeaders(),
        StdBody(htmxComponent, url=pageData.path)
      )
      htmxComponent.collectHtml(htmlFragments)
  kwargs = htmxComponent.kwargs
  # print("-------------------------------------------------")
  # print('\n'.join(htmlFragments))
  # print("-------------------------------------------------")
  return HTMLResponse('\n'.join(htmlFragments), **kwargs)


# NOTE the registered home page func MUST return a RefreshMainContent
# object

homePageFunc = None
def registerHomePage(aHomePageFunc) :
  global homePageFunc
  homePageFunc = aHomePageFunc

def goToHomePage(pageData, **kwargs) :
  return homePageFunc(pageData, **kwargs)

async def callWithParameters(request, func, anyUser=False) :
  params = {}
  if request.query_params :
    params.update(request.query_params)
  if request.path_params :
    params.update(request.path_params)
  # print("----------------------------")
  # print(yaml.dump(params))
  # print("----------------------------")

  dbPath = ":memory:"
  if 'database' in config :
    dbPath = config['database']
  try :
    db = sqlite3.connect(dbPath)
    pageData = PageData(db)
    await pageData.getRequestData(request)
    if anyUser or pageData.user.is_authenticated :
      htmxComponent = func(pageData, **params)
    elif homePageFunc :
      message = "You must be logged in to access that page"
      if 'develop' in config :
        message += f" ({request.url.path})"
      htmxComponent = homePageFunc(
        pageData
      ).addMessage(
        WarnFooterMessage(Text(message)),
      )
    else :
      raise HTTPException(
        404,
        detail=f"No home page registered while trying to serve {request.url.path}"  # noqa
      )

    if pageData.login :
      await login_user(request, pageData.login)
    elif pageData.logout :
      await logout_user(request)

    return htmlResponseFromHtmx(htmxComponent, pageData)
  finally :
    db.close()

def getRoute(aRoute, getFunc, anyUser=False, name=None) :
  @wraps(getFunc)
  async def getWrapper(request) :
    print(f"Any user: {anyUser}")
    return await callWithParameters(request, getFunc, anyUser=anyUser)
  routes.append(SSLRoute(
    aRoute, getWrapper, anyUser=anyUser, name=name, methods=["GET"]
  ))

def putRoute(aRoute, putFunc, anyUser=False, name=None) :
  @wraps(putFunc)
  async def putWrapper(request) :
    return await callWithParameters(request, putFunc, anyUser=anyUser)
  routes.append(SSLRoute(
    aRoute, putWrapper, anyUser=anyUser, name=name, methods=["PUT", "POST"]
  ))

def postRoute(aRoute, postFunc, anyUser=False, name=None) :
  @wraps(postFunc)
  async def postWrapper(request) :
    return await callWithParameters(request, postFunc, anyUser=anyUser)
  routes.append(SSLRoute(
    aRoute, postWrapper, anyUser=anyUser, name=name, methods=["POST"]
  ))

def patchRoute(aRoute, patchFunc, anyUser=False, name=None) :
  @wraps(patchFunc)
  async def patchWrapper(request) :
    return await callWithParameters(request, patchFunc, anyUser=anyUser)
  routes.append(SSLRoute(
    aRoute, patchWrapper, anyUser=anyUser, name=name, methods=["PATCH", "POST"]
  ))

def deleteRoute(aRoute, deleteFunc, anyUser=False, name=None) :
  @wraps(deleteFunc)
  async def deleteWrapper(request) :
    return await callWithParameters(request, deleteFunc, anyUser=anyUser)
  routes.append(SSLRoute(
    aRoute, deleteWrapper, anyUser=anyUser,
    name=name, methods=["GET", "DELETE"]
  ))

###############################################################
# Capture the "external facing" page parts

pageParts = {}

# regexp tester: https://pythex.org/
regExps = [
  r"(?P<level>Level.div)",
  r"hxTarget\s*=\s*'(?P<hxTarget>[^\']*)'",
  r"Link\(\s*f?'(?P<link>[^\']*)'",
  r"hxGet\s*=\s*f?'(?P<hxGet>[^\']*)'",
  r"hxPost\s*=\s*(?P<hxPost>[^\s,]*)",
  r"schoolLib\.(?P<pagePart>[^\(\s]*)\s*\(\s*pageData",
  r"callPagePart\(\s*\'(?P<callPagePart>[^\']*)\'"
]
metaDataRegExp = re.compile('|'.join(regExps))
# '

class PagePart :
  def __init__(self, func) :
    self.users = set()
    self.func  = func
    name       = str(func.__module__) + '.' + str(func.__name__)
    self.name  = name.lstrip('schoolLib.')
    pageParts[self.name] = self

  def addUser(self, aUser) :
    self.users.add(aUser)

  def collectMetaData(self) :
    self.sig  = str(signature(self.func))
    self.doc  = getdoc(self.func)
    if not self.doc :
      self.doc = "No doc string"
    src  = getsource(self.func)
    metaData = []
    for aMatch in metaDataRegExp.finditer(src) :
      metaData.append(aMatch.groupdict())
    self.metaData = metaData
    self.src = src

def pagePart(func) :
  PagePart(func)  # register this pagePart
  return func

def computePagePartUsers() :

  # compute the users from each route
  for aRoute in routes :
    aPath = aRoute.path
    anEndpoint = str(aRoute.endpoint.__module__) + \
      '.' + str(aRoute.endpoint.__name__)
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
          print(f"Could not find page part {someMetaData['callPagePart']} in {pagePartName}")  # noqa
          continue
        pageParts[someMetaData['callPagePart']].addUser(pagePartName)
