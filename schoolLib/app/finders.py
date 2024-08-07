
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# borrowers

@pagePart
async def findABorrower(request, db, probe=None, nameRows=[], **kwargs) :
  return Level2div([
    SearchBox(
      hxPost='/search/borrowers',
      name='search',
      value=probe,
      placeholder="Type a person's name"
    ),
    Table(nameRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@pagePart
async def getFindBorrowerForm(request, db, **kwargs) :
  return Level1div([
    await callPagePart('app.menus.secondLevelPeopleMenu', request, db, selectedId='findBorrower'),
    await callPagePart(
      'app.finders.findABorrower',
      request, db, **kwargs
    )
  ])

getRoute('/search/borrowers', getFindBorrowerForm)

@pagePart
async def postSearchForBorrower(request, db, **kwargs) :
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
      hxTarget='#level2div'
    ))))
  return await callPagePart(
    'app.finders.findABorrower',
    request, db,
    probe=theForm['search'], nameRows=nameRows,
    **kwargs
  )

postRoute('/search/borrowers', postSearchForBorrower)

##########################################################################
# items (aka Books)

@pagePart
async def findAnItem(request, db, probe=None, itemRows=[], **kwargs) :
  return Level2div([
    SearchBox(
      hxPost='/search/items',
      name='search',
      value=probe,
      placeholder='Type a book title...'
    ),
    Table(itemRows, theId='searchResults')
  ], attrs={'hx-ext':'morph'})

@pagePart
async def getFindAnItemForm(request, db, **kwargs) :
  return Level1div([
    await callPagePart('app.menus.secondLevelBooksMenu', request, db, selectedId='findBook'),
    await callPagePart(
      'app.finders.findAnItem',
      request, db, **kwargs
    )
  ])

getRoute('/search/items', getFindAnItemForm)

@pagePart
async def postSearchForAnItem(request, db, **kwargs) :
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
      hxTarget='#level2div'
    ))))
  return await callPagePart(
    'app.finders.findAnItem',
    request, db,
    probe=theForm['search'], itemRows=itemRows,
    **kwargs
  )

postRoute('/search/items', postSearchForAnItem)
