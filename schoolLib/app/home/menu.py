
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

@get('/menu/home')
def homeMenu(request) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return HTMXResponse(
    request,
    level0div([
      htmxMenu(topLevelMenu, selected='home'),
      level1div(markdownDiv(homePageMarkdown))
    ], theId='level0div')
  )
