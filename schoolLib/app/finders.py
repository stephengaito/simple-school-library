
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus
import schoolLib.app.people.menu
import schoolLib.app.books.menu

##########################################################################
# borrowers

@pagePart
def findABorrower(pageData, probe=None, nameRows=[], **kwargs) :
  return Level2div([
    SearchBox(
      hxPost='/search/borrowers',
      name='search',
      helpName='findBorrower',
      value=probe,
      placeholder="Type a person's name"
    ),
    Table(nameRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@pagePart
def getFindBorrowerForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='findBorrower'
    ),
    schoolLib.app.finders.findABorrower(pageData, **kwargs)
  ])

getRoute('/search/borrowers', getFindBorrowerForm, anyUser=True)

@pagePart
def postSearchForBorrower(pageData, **kwargs) :
  theForm = pageData.form
  nameRows =[]
  selectSql = SelectSql(
  ).fields(
    'borrowerId', 'firstName', 'familyName'
  ).tables('borrowersFTS'
  ).limitTo(10
  ).orderBy('rank')
  if theForm['search'] :
    selectSql.whereValue(
      'borrowersFTS', theForm['search']+'*', operator='MATCH'
    )
  print(selectSql.sql())
  results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
  for aRow in results :
    nameRows.append(TableRow(TableEntry(Link(
      f'/borrowers/show/{aRow['borrowerId']}',
      f'{aRow['firstName']} {aRow['familyName']}',
      hxTarget='#level2div'
    ))))
  return schoolLib.app.finders.findABorrower(
    pageData,
    probe=theForm['search'], nameRows=nameRows,
    **kwargs
  )

postRoute('/search/borrowers', postSearchForBorrower, anyUser=True)

##########################################################################
# items (aka Books)

@pagePart
def findAnItem(pageData, probe=None, itemRows=[], **kwargs) :
  return Level2div([
    SearchBox(
      hxPost='/search/items',
      name='search',
      helpName='findBook',
      value=probe,
      placeholder='Type a book title...'
    ),
    Table(itemRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@pagePart
def getFindAnItemForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, selectedId='findBook'
    ),
    schoolLib.app.finders.findAnItem(pageData, **kwargs)
  ])

getRoute('/search/items', getFindAnItemForm, anyUser=True)

@pagePart
def postSearchForAnItem(pageData, **kwargs) :
  theForm = pageData.form
  itemRows = []
  selectSql = SelectSql(
  ).fields(
    'itemsInfoId', 'title'
  ).tables(
    'itemsFTS'
  ).limitTo(10
  ).orderBy('rank')
  if theForm['search'] :
    selectSql.whereValue(
      'itemsFTS', theForm['search']+'*', operator='MATCH'
    )
  print(selectSql.sql())
  results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
  for aRow in results :
    itemRows.append(TableRow(TableEntry(Link(
      f'/itemsInfo/show/{aRow['itemsInfoId']}',
      aRow['title'],
      hxTarget='#level2div'
    ))))
  return schoolLib.app.finders.findAnItem(
    pageData,
    probe=theForm['search'], itemRows=itemRows,
    **kwargs
  )

postRoute('/search/items', postSearchForAnItem, anyUser=True)
