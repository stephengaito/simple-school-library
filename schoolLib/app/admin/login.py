
from schoolLib.setup          import *
from schoolLib.htmxComponents import *
import schoolLib.app.main

@pagePart
def getLoginForm(pageData, message="Please login", **kwargs) :
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
    ], "Login", hxTarget='#level0div', hxPost='/login')
  ])

getRoute('/login', getLoginForm, anyUser=True)
registerLoginPage(getLoginForm)

@pagePart
def postLoginPage(pageData, **kwargs) :
  theForm = pageData.form
  user = OtherUser()
  if theForm['userName'] == 'slib' :
    if authenticateSlibUser(theForm['userPassword'], pageData.db) :
      user = SLibUser()
  print(f"Logged in user: {user.display_name}")
  pageData.setUser(user)
  return schoolLib.app.main.homePage(pageData, hxTarget='#level0div')

postRoute('/login', postLoginPage, anyUser=True)

@pagePart
def logoutPage(pageData, **kwargs) :
  if pageData.user.is_authenticated : pageData.shouldLogout()
  return schoolLib.app.main.homePage(pageData, hxTarget='#level0div')

getRoute('/logout', logoutPage, anyUser=True)
