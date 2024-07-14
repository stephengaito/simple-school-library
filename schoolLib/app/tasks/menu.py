
from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelTasksMenu = [
  { 'component' : 'button',
    'c-name' : 'booksCheckedOut',
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
      htmxMenu(topLevelMenu, selected='tasks'),
      level1div([
        htmxMenu(secondLevelTasksMenu, selected='booksCheckedOut'),
        markdownDiv(tasksMarkdown)
      ])
    ], theId='level0div')
  )
