
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@pagePart
def homeMenu(request, db) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(homePageMarkdown))
  ], theId='level0div')

getRoute('/menu/home', homeMenu)
