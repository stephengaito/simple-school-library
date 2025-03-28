
from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Menu, Button, Level0div, Level1div, \
  getHelpPage
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
        hxTarget = '#level0div'
      )
    )
  else :
    theMenu.appendAChild(
      Button(
        'Login',
        theId    = 'login',
        hxGet    = '/login',
        hxTarget = '#level0div'
      )
    )
  return theMenu

@pagePart
def adminMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='admin'),
    Level1div([
      secondLevelAdminMenu(pageData, **kwargs),
      getHelpPage(
        pageData, 'adminPage', modal=False,
        hxPost='/editHelp/adminPage/nonModal'
      )

    ])
  ], theId='level0div')

##########################################################################
# routes

getRoute('/menu/admin', adminMenu, anyUser=True)

