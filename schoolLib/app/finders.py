
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *

##########################################################################
# borrowers

def findABorrower(probe, nameRows) :
  return Level2div([
    SearchBox(
      post='/search/borrowers',
      name='search',
      value=probe,
      placeholder="Type a person's name"
    ),
    Table(nameRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@get('/search/borrowers')
def getFindBorrowerForm(request, db) :
  return Level1div([
    SecondLevelPeopleMenu.select('findBorrower'),
    findABorrower(None, [])
  ])

@post('/search/borrowers')
async def postSearchForBorrower(request, db) :
  theForm = await request.form()
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
  results = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in results :
    nameRows.append(TableRow(TableEntry(Link(
      f'/borrowers/show/{aRow['borrowerId']}',
      f'{aRow['firstName']} {aRow['familyName']}',
      target='#level2div'
    ))))
  return findABorrower(theForm['search'], nameRows)

##########################################################################
# items (aka Books)

def findAnItem(probe, itemRows) :
  return Level2div([
    SearchBox(
      post='/search/items',
      name='search',
      value=probe,
      placeholder='Type a book title...'
    ),
    Table(itemRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@get('/search/items')
def getFindAnItemForm(request, db) :
  return Level1div([
    SecondLevelBooksMenu.select('findBook'),
    findAnItem(None, [])
  ])

@post('/search/items')
async def postSearchForAnItem(request, db) :
  theForm = await request.form()
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
  results = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in results :
    itemRows.append(TableRow(TableEntry(Link(
      f'/itemsInfo/show/{aRow['itemsInfoId']}',
      aRow['title'],
      target='#level2div'
    ))))
  return findAnItem(theForm['search'], itemRows)
