
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *

##########################################################################
# borrowers

def findABorrower(probe, nameRows) :
  return level2div([
    searchBox(
      post='/search/borrowers',
      name='search',
      value=probe,
      placeholder="Type a person's name"
    ),
    table(nameRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@get('/search/borrowers')
def getFindBorrowerForm(request) :
  return HTMXResponse(
    request,
    level1div([
      menu(secondLevelPeopleMenu, selected='findBorrower'),
      findABorrower(None, [])
    ])
  )

@post('/search/borrowers')
async def postSearchForBorrower(request) :
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
  with getDatabase() as db :
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    for aRow in results :
      nameRows.append(tableRow(tableEntry(link(
        f'/borrowers/show/{aRow['borrowerId']}',
        f'{aRow['firstName']} {aRow['familyName']}',
        target='#level2div'
      ))))
  return HTMXResponse(
    request,
    findABorrower(theForm['search'], nameRows)
  )

##########################################################################
# items (aka Books)

def findAnItem(probe, itemRows) :
  return level2div([
    searchBox(
      post='/search/items',
      name='search',
      value=probe,
      placeholder='Type a book title...'
    ),
    table(itemRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@get('/search/items')
def getFindAnItemForm(request) :
  return HTMXResponse(
    request,
    level1div([
      menu(secondLevelBooksMenu, selected='findBook'),
      findAnItem(None, [])
    ])
  )

@post('/search/items')
async def postSearchForAnItem(request) :
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
  with getDatabase() as db :
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    for aRow in results :
      itemRows.append(tableRow(tableEntry(link(
        f'/itemsInfo/show/{aRow['itemsInfoId']}',
        aRow['title'],
        target='#level2div'
      ))))
  return HTMXResponse(
    request,
    findAnItem(theForm['search'], itemRows)
  )
