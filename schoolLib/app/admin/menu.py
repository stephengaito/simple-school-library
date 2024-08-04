
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

##########################################################################
# routes

@pagePart
async def adminMenu(request, db, **kwargs) :
  tasksMarkdown = "somthing about **admin**"

  return Level0div([
    await callPagePart(
      'app.menus.topLevelMenu', request, db, selectedId='admin'
    ),
    Level1div([
      await callPagePart(
        'app.menus.secondLevelAdminMenu', request, db, **kwargs
      )
    ])
  ], theId='level0div')

getRoute('/menu/admin', adminMenu)

