
from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelPeopleMenu = [
  { 'component' : 'button',
    'c-name' : 'add',
    'text' : 'Add a person',
    'get'  : '/menu/people/add'
  },
]

@get('/menu/people')
def peopleMenu(request) :
  peopleMarkdown = "somthing about **people**"

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='people'),
      level1div([
        menu(secondLevelPeopleMenu, selected='add'),
        markdownDiv(peopleMarkdown)
      ])
    ], theId='level0div')
  )
