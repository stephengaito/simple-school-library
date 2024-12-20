
from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Menu, Button, Level0div, Level1div, \
  getHelpPage
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelPeopleMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'Find a person',
      theId    = 'findBorrower',
      hxGet    = '/search/borrowers',
      hxTarget = '#level1div'
    )
  ], klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendChildren([
      Button(
        'Add a person',
        theId    = 'addBorrower',
        hxGet    = '/menu/people/addBorrower',
        hxTarget = '#level1div'
      ),
      Button(
        'List classes',
        theId    = 'listClasses',
        hxGet    = '/menu/people/listClasses',
        hxTarget = '#level1div'
      ),
      Button(
        'Add a class',
        theId    = 'addClass',
        hxGet    = '/menu/people/addClass',
        hxTarget = '#level1div'
      )
    ])

  if selectedId : theMenu.select(selectedId)

  return theMenu

@pagePart
def secondLevelSinglePersonMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([], klassName='vertical')

  # return book

  # edit this person
  # delete this person

  if pageData.user.is_authenticated :
    pass

  if selectedId : theMenu.select(selectedId)

  return theMenu


##########################################################################
# routes

@pagePart
def peopleMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    Level1div([
      secondLevelPeopleMenu(pageData),
      getHelpPage(
        pageData, 'peoplePage', modal=False,
        hxPost='/editHelp/peoplePage/nonModal'
      )
    ])
  ], theId='level0div')

getRoute('/menu/people', peopleMenu, anyUser=True)
