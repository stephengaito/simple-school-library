
from schoolLib.setup import *
from schoolLib.htmxComponents import *

secondLevelPeopleMenu = [
  { 'component' : 'button',
    'c-name' : 'addClass',
    'text' : 'Add a class',
    'get'  : '/menu/people/addClass'
  },
  { 'component' : 'button',
    'c-name' : 'listClasses',
    'text' : 'List classes',
    'get'  : '/menu/people/listClasses'
  },
  { 'component' : 'button',
    'c-name' : 'addBorrower',
    'text' : 'Add a person',
    'get'  : '/menu/people/addBorrower'
  },
  { 'component' : 'button',
    'c-name' : 'findBorrower',
    'text' : 'Find a person',
    'get'  : '/menu/people/addBorrower'
  },
]

def editClassForm(
  className=None, classDesc=None, classOrder=None, classColour=None,
  submitMessage="Save changes", postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- htmxForm with NO postUrl -->"

  return htmxForm([
    textInput(
      label='Class name',
      name='className',
      value=className,
      placeholder='A class name...'
    ),
    textInput(
      label='Description',
      name='classDesc',
      value=classDesc,
      placeholder='A description of your class...'
    ),
    numberInput(
      label='Class order',
      name='classOrder',
      value=classOrder,
      defaultValue=0
    ),
    colourInput(
      label='Class colour',
      name='classColour',
      value=classColour,
      defaultValue='#000000'
    )
  ], submitMsg=submitMessage, post=postUrl, **kwargs)

def addAClass() :
  return level1div([
    htmxMenu(secondLevelPeopleMenu, selected='addClass', hxAttrs={
      'hx-target' : '#level1div'
    }),
    editClassForm(submitMessage='Add new class', postUrl='/classes/new')
  ])

@get('/menu/people')
def peopleMenu(request) :

  return HTMXResponse(
    request,
    level0div([
      htmxMenu(topLevelMenu, selected='people'),
      addAClass()
    ], theId='level0div')
  )

@get('/menu/people/addClass')
def addAClassMenu(request) :
  return HTMXResponse(
    request,
    addAClass()
  )