
from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelTasksMenu = [
  { 'component' : 'button',
    'text' : 'Books checked out',
    'get'  : '/menu/tasks/booksCheckedOut'
  },
]

@get('/menu/tasks')
def tasksMenu(request) :
  tasksMarkdown = "somthing about **tasks**"

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected=0),
      level1div([
        menu(secondLevelTasksMenu, selected=0),
        markdownDiv(tasksMarkdown)
      ])
    ], theId='level0div')
  )
