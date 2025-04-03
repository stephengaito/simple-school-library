
from schoolLib.setup import pagePart, getRoute
from schoolLib.htmxComponents import Menu, Button, MainContent, \
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
    )
  ], klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendChildren([
      Button(
        'Add a person',
        theId    = 'addBorrower',
        hxGet    = '/menu/people/addBorrower',
      ),
      Button(
        'List classes',
        theId    = 'listClasses',
        hxGet    = '/menu/people/listClasses',
      ),
      Button(
        'Add a class',
        theId    = 'addClass',
        hxGet    = '/menu/people/addClass',
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
  return MainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    secondLevelPeopleMenu(pageData),
    getHelpPage(
      pageData, 'peoplePage', modal=False,
      hxPost='/editHelp/peoplePage/nonModal'
    )
  )

getRoute('/menu/people', peopleMenu, anyUser=True)
