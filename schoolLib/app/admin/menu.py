
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

##########################################################################
# routes

@pagePart
def adminMenu(pageData, **kwargs) :
  tasksMarkdown = "somthing about **admin**"

  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='admin'),
    Level1div([
      schoolLib.app.menus.secondLevelAdminMenu(pageData, **kwargs)
    ])
  ], theId='level0div')

getRoute('/menu/admin', adminMenu)

