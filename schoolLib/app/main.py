
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
async def homePage(request, db, **kwargs):
  """ The Home Page """
  return HtmlPage(
    StdHeaders(),
    StdBody()
  )

getRoute('/', homePage, anyUser=True)

@pagePart
async def helpPages(request, db, aPath=None, **kwargs) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return Level0div([
    await callPagePart(
      'app.menus.topLevelMenu', request, db, selectedId='home', **kwargs
    ),
    Level1div(MarkdownDiv(someMarkdown))
  ])

getRoute('/help/{aPath:path}', helpPages, anyUser=True)

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    await callPagePart('app.menus.topLevelMenu', request, None, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!"),
      Text(f"Looking for: [{request.url}]")
    ])
  ], status_code=404), request)

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    await callPagePart('app.menus.topLevelMenu', request, None, selectedId='home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!", type='p'),
      Text(f"Looking for: [{request.url}]", type='p'),
      Text(f"Error: {repr(theException)}", type="p"),
    ])
  ], status_code=500), request)


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

