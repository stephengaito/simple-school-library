
# import os
# import yaml

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
# from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from starlette_login.backends import SessionAuthBackend
from starlette_login.login_manager import Config as LoginManagerConfig
from starlette_login.login_manager import LoginManager
from starlette_login.login_manager import ProtectionLevel
from starlette_login.middleware import AuthenticationMiddleware

from schoolLib.setup import loadedConfig, PageData, htmlResponseFromHtmx, \
  loadUsers, config, routes

from schoolLib.htmxComponents import loadedTheme, RefreshMainContent, Text

import schoolLib.app.menus

loadedConfig('config.yaml', verbose=True)
loadedTheme()

# The ORDER here is important!
import schoolLib.app.utils
import schoolLib.app.home.home
import schoolLib.app.books
import schoolLib.app.people
import schoolLib.app.tasks
import schoolLib.app.admin

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  pageData = PageData(None)
  await pageData.getRequestData(request)
  return htmlResponseFromHtmx(
    RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
      None,
      [
        Text("Opps! Something went wrong! We can't find that page!"),
        Text(f"Looking for: [{request.url}]")
      ],
      status_code=404
    ), pageData
  )

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  pageData = PageData(None)
  await pageData.getRequestData(request)
  return htmlResponseFromHtmx(
    RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
      None,
      [
        Text("Opps! Something went wrong! We can't find that page!", type='p'),
        Text(f"Looking for: [{request.url}]", type='p'),
        Text(f"Error: {repr(theException)}", type="p"),
      ],
      status_code=500
    ), pageData
  )


# see: https://starlette-login.readthedocs.io/en/stable/usage/
sessionSecretKey = config['secretKey']
sessionMaxAge = 10 * 60  # 10 minutes
if 'sessionMaxAge' in config :
  sessionMaxAge    = config['sessionMaxAge']
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
    Middleware(
      SessionMiddleware,
      secret_key=sessionSecretKey,
      max_age=sessionMaxAge
    ),
    Middleware(
      AuthenticationMiddleware,
      backend=SessionAuthBackend(loginManager),
      login_manager=loginManager,
    )
  ]
)
app.state.login_manager = loginManager
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

def setupApp() :
  pass
