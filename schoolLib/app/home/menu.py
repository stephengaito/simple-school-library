
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

@pagePart
def getHomeMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div(
      getHelpPage(pageData, '/menu/home', hxPost='/editHelp/menu/home'),
      klassName='gridless'
    )
  ], theId='level0div')

getRoute('/menu/home', getHomeMenu, anyUser=True)

postRoute('/menu/home',
  lambda pageData : postHelpPage(pageData, 'homePage', hxPost='/menu/home')
)
