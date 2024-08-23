
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelPeopleMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'List classes',
      theId    = 'listClasses',
      hxGet    = '/menu/people/listClasses',
      hxTarget = '#level1div'
    ),
    Button(
      'Find a person',
      theId    = 'findBorrower',
      hxGet    = '/search/borrowers',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendChild(
      Button(
        'Add a person',
        theId    = 'addBorrower',
        hxGet    = '/menu/people/addBorrower',
        hxTarget = '#level1div'
      )
    )

    theMenu.appendChild(
      Button(
        'Add a class',
        theId    = 'addClass',
        hxGet    = '/menu/people/addClass',
        hxTarget = '#level1div'
      )
    )

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
