
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

@pagePart
def getHomeMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div(
      getHelpPage(
        pageData, 'homePage', modal=False,
        hxPost='/editHelp/homePage/nonModal'),
      klassName='gridless'
    )
  ], theId='level0div')

getRoute('/menu/home', getHomeMenu, anyUser=True)

#postRoute('/menu/home',
#  lambda pageData : postHelpPage(pageData, 'homePage', hxPost='/menu/home')
#)
