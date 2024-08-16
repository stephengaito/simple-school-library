
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@pagePart
def getHomeMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div(getHelpPage('homePage'), klassName='gridless')
  ], theId='level0div')

getRoute('/menu/home',
  lambda pageData : getHelpPage(pageData, 'homePage', hxPost='/menu/home'),
  anyUser=True
)

postRoute('/menu/home',
  lambda pageData : postHelpPage(pageData, 'homePage')
)
