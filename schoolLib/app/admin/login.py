
from starlette_login.utils import login_user, logout_user

from schoolLib.setup          import *
from schoolLib.htmxComponents import *

@pagePart
async def getLoginForm(request, db, message="Please login", **kwargs) :
  return Level0div([
    Text(message),
    FormTable([
      TextInput(
        label='User name',
        name='userName',
        placeholder='A user name...'
      ),
      PasswordInput(
        label='User password',
        name='userPassword',
      )
    ], "Login", hxTarget='this', hxPost='/login')
  ])

getRoute('/login', getLoginForm, anyUser=True)
registerLoginPage(getLoginForm)

@pagePart
async def postLoginPage(request, db, **kwargs) :
  theForm = await request.form()
  user = OtherUser()
  if theForm['userName'] == 'slib' :
    if authenticateSlibUser(theForm['userPassword'], db) :
      user = SLibUser()
  print(f"Logged in user: {user.display_name}")
  await login_user(request, user)
  return await callPagePart('app.main.homePage', request, db, **kwargs)

postRoute('/login', postLoginPage, anyUser=True)

@pagePart
async def logoutPage(request, db, **kwargs) :
  if request.user.is_authenticated :
    await logout_user(request)
  return await callPagePart('app.main.homePage', request, db, **kwargs)

getRoute('/logout', logoutPage)

async def GoToLoginPage(request, db, **kwargs) :
  return await callPagePart(
    'app.login.getLoginForm', request, db, **kwargs
  )
