
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@pagePart
async def homeMenu(request, db, **kwargs) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(homePageMarkdown))
  ], theId='level0div')

getRoute('/menu/home', homeMenu)
