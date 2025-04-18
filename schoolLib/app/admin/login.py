
from schoolLib.setup          import pagePart, getRoute, postRoute, \
  OtherUser, authenticateSlibUser, SLibUser, goToHomePage

from schoolLib.htmxComponents import RefreshMainContent, Text, \
  FormTable, TextInput, PasswordInput, OKFooterMessage
import schoolLib.app.main
import schoolLib.app.menus
import schoolLib.app.admin.menu

@pagePart
def getLoginForm(pageData, message="Please login", **kwargs) :
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='admin'),
    schoolLib.app.admin.menu.secondLevelAdminMenu(
      pageData, selectedId='login'
    ),
    [
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
      ], "Login", hxPost='/login')
    ]
  )

getRoute('/login', getLoginForm, anyUser=True)

@pagePart
def postLoginPage(pageData, **kwargs) :
  theForm = pageData.form
  user = OtherUser()
  if theForm['userName'] == 'slib' :
    if authenticateSlibUser(theForm['userPassword'], pageData.db) :
      user = SLibUser()
  loginMessage = f"You are now logged in as the user: {user.display_name}"
  print(loginMessage)
  pageData.setUser(user)
  return goToHomePage(pageData).addMessage(
    OKFooterMessage(loginMessage)
  )

postRoute('/login', postLoginPage, anyUser=True)

@pagePart
def logoutPage(pageData, **kwargs) :
  if pageData.user.is_authenticated : pageData.shouldLogout()
  return goToHomePage(pageData).addMessage(
    OKFooterMessage("You are now logged out")
  )

getRoute('/logout', logoutPage, anyUser=True)
