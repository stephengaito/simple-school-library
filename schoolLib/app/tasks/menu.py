
from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Menu, Button, getHelpPage, \
  MainContent
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
    )
  ], selectedId=selectedId, klassName='vertical')

##########################################################################
# routes

@pagePart
def tasksMenu(pageData, **kwargs) :

  return MainContent(
    schoolLib.app.menus.topLevelMenu(
      pageData, selectedId='tasks'
    ),
    secondLevelTasksMenu(pageData),
    getHelpPage(
      pageData, 'tasksMenu', modal=False,
      hxPost='/editHelp/tasksMenu/nonModal'),
  )

getRoute('/menu/tasks', tasksMenu, anyUser=True)
