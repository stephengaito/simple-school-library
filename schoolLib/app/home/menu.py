
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@pagePart
async def getHomeMenu(request, db, **kwargs) :
  return Level0div([
    await callPagePart('app.menus.topLevelMenu', request, db, selectedId='home'),
    Level1div(getHelpPage('homePage'), klassName='gridless')
  ], theId='level0div')

getRoute('/menu/home',
  lambda request, db : getHelpPage(request, db, 'homePage', hxPost='/menu/home'),
  anyUser=True
)

postRoute('/menu/home',
  lambda request, db : postHelpPage(request, db, 'homePage')
)
