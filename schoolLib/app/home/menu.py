
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelHomeMenu(pageData, selectedId=None, **kwargs) :
  return Menu([], selectedId=selectedId, klassName='vertical')

@pagePart
def getHomeMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div([
      secondLevelHomeMenu(pageData),
      getHelpPage(
        pageData, 'homePage', modal=False,
        hxPost='/editHelp/homePage/nonModal'
      )
    ])
  ], theId='level0div')

##########################################################################
# routes

getRoute('/menu/home', getHomeMenu, anyUser=True)

registerHomePage(getHomeMenu)
