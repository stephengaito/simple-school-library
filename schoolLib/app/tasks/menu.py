
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelTasksMenu(pageData, selectedId=None, **kwargs) :
  return Menu([
    Button(
      'Books checked out',
      theId    = 'booksCheckedOut',
      hxGet    = '/menu/tasks/booksCheckedOut',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

##########################################################################
# routes

@pagePart
def tasksMenu(pageData, **kwargs) :

  return Level0div([
    schoolLib.app.menus.topLevelMenu(
      pageData, selectedId='tasks'
    ),
    Level1div([
      secondLevelTasksMenu(pageData),
      getHelpPage(
        pageData, 'tasksMenu', modal=False,
        hxPost='/editHelp/tasksMenu/nonModal'),
    ])
  ])

getRoute('/menu/tasks', tasksMenu, anyUser=True)
