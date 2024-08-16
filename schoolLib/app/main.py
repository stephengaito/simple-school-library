
import os
import yaml

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from starlette_login.backends import SessionAuthBackend
from starlette_login.login_manager import Config as LoginManagerConfig
from starlette_login.login_manager import LoginManager
from starlette_login.login_manager import ProtectionLevel
from starlette_login.middleware import AuthenticationMiddleware

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

loadedConfig('config.yaml', verbose=True)
loadedTheme()

# The ORDER here is important!
import schoolLib.app.home.menu
import schoolLib.app.books
import schoolLib.app.people
import schoolLib.app.tasks.menu
import schoolLib.app.metaStructure
import schoolLib.app.admin

@pagePart
def homePage(pageData, **kwargs):
  """ The Home Page """
  return HtmlPage(
    StdHeaders(),
    StdBody()
  )

getRoute('/', homePage, anyUser=True)

@pagePart
def helpPages(pageData, aPath=None, **kwargs) :
  if not aPath : aPath = '/'
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home', **kwargs),
    Level1div([
      schoolLib.app.menus.secondLevelHelpMenu(pageData, aPath),
      getHelpPage(pageData, aPath, hxPost=f'/editHelp{aPath}')
    ])
  ])

getRoute('/help{aPath:path}', helpPages, anyUser=True)

@pagePart
def editHelpPage(pageData, aPath=None, **kwargs) :
  if not aPath : aPath = '/'
  helpPageHtml = getHelpPageHtml(pageData.db, aPath)
  print(helpPageHtml)
  return Level1div([
    Div([]),
    HelpEditorForm(
      helpPageHtml, aPath, f'/editHelp{aPath}', hxTarget='#level1div'
    )
  ])

getRoute('/editHelp{aPath:path}', editHelpPage)

@pagePart
def postHelpPages(pageData, aPath=None, **kwargs) :
  if not aPath : aPath = '/'
  return postHelpPage(
    pageData, aPath,
    hxPost=f'/editHelp{aPath}', hxTarget='#level1div',
    **kwargs
  )

postRoute('/editHelp{aPath:path}', postHelpPages)

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  pageData = PageData(None)
  await pageData.getRequestData(request)
  return htmlResponseFromHtmx(Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!"),
      Text(f"Looking for: [{request.url}]")
    ])
  ], status_code=404), pageData)

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  pageData = PageData(None)
  await pageData.getRequestData(request)
  return htmlResponseFromHtmx(Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!", type='p'),
      Text(f"Looking for: [{request.url}]", type='p'),
      Text(f"Error: {repr(theException)}", type="p"),
    ])
  ], status_code=500), pageData)


# see: https://starlette-login.readthedocs.io/en/stable/usage/
sessionSecretKey = config['secretKey']
loginManagerConfig = LoginManagerConfig(
  protection_level=ProtectionLevel.Strong
)
loginManager = LoginManager(
  redirect_to='/login_endpoint',
  secret_key=sessionSecretKey,
  config=loginManagerConfig
)
loginManager.set_user_loader(loadUsers)

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  },
  middleware=[
    Middleware(SessionMiddleware, secret_key=sessionSecretKey),
    Middleware(
      AuthenticationMiddleware,
      backend=SessionAuthBackend(loginManager),
      login_manager=loginManager,
    )
  ]
)
app.state.login_manager = loginManager
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

