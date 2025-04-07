
from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Menu, Button, \
  RefreshMainContent, getHelpPage
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelAdminMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([], klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendAChild(
      Button(
        'Logout',
        theId    = 'logout',
        hxGet    = '/logout',
      )
    )
  else :
    theMenu.appendAChild(
      Button(
        'Login',
        theId    = 'login',
        hxGet    = '/login',
      )
    )
  return theMenu

@pagePart
def adminMenu(pageData, **kwargs) :
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='admin'),
    secondLevelAdminMenu(pageData, **kwargs),
    getHelpPage(
      pageData, 'adminPage', modal=False,
      hxPost='/editHelp/adminPage/nonModal'
    )
  )

##########################################################################
# routes

getRoute('/menu/admin', adminMenu, anyUser=True)

