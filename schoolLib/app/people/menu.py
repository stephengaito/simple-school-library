
from schoolLib.setup import *
from schoolLib.htmxComponents import *
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

@pagePart
def getFindBorrowerForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='findBorrower'
    ),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      theId='level2div', hxPost='/search/borrowers',
      helpName='findBorrower', placeHolder="Type a person's name",
      **kwargs
    )
  ])

getRoute('/search/borrowers', getFindBorrowerForm, anyUser=True)

class SearchForABorrowerIter(schoolLib.app.utils.finders.SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
    selectSql = SelectSql(
    ).fields(
      'borrowerId', 'firstName', 'familyName'
    ).tables('borrowersFTS'
    ).limitTo(10
    ).orderAscBy('rank')
    if theForm['search'] :
      selectSql.whereValue(
        'borrowersFTS', theForm['search']+'*', operator='MATCH'
      )
    print(selectSql.sql())
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    return (
      f'{self.targetUrl}/{curRow['borrowerId']}',
      f'{curRow['firstName']} {curRow['familyName']}'
    )

@pagePart
def postSearchForBorrower(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, SearchForABorrowerIter,
    hxTarget='#level1div', targetUrl='/borrowers/show',
    theId='level2div', hxPost='/search/borrowers',
    helpName='findBorrower', placeHolder="Type a person's name",
    **kwargs
  )

postRoute('/search/borrowers', postSearchForBorrower, anyUser=True)
