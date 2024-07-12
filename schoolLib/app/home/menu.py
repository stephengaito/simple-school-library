
from schoolLib.setup import *
from schoolLib.htmxComponents import *

@get('/menu/home')
def homeMenu(request) :
  homePageMarkdown = loadMarkdownFromFile('homePage')

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='home'),
      level1div(markdownDiv(homePageMarkdown))
    ], theId='level0div')
  )
