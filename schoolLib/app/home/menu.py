
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@pagePart
async def homeMenu(request, db, **kwargs) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return Level0div([
    await callPagePart('app.menus.topLevelMenu', request, db, selectedId='home'),
    Level1div(MarkdownDiv(homePageMarkdown), klassName='gridless')
  ], theId='level0div')

getRoute('/menu/home', homeMenu)
