
from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelPeopleMenu = [
  { 'component' : 'button',
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
      menu(topLevelMenu, selected=0),
      level1div([
        menu(secondLevelPeopleMenu, selected=0),
        markdownDiv(peopleMarkdown)
      ])
    ], theId='level0div')
  )
