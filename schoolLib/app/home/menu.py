
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@get('/menu/home')
def homeMenu(request, db) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(homePageMarkdown))
  ], theId='level0div')
