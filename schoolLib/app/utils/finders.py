
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *

import schoolLib

##########################################################################
# generic finder (get front end)

@pagePart
def findAThing(
  pageData, probe=None, thingRows=[],
  theId='level2div', hxPost='/search/borrowers',
  helpName='findBorrower', placeHolder="Type a person's name",
  **kwargs
) :
  hxTarget = '#'+theId
  return Div([
    SearchBox(
      hxPost=hxPost,
      name='search',
      helpName=helpName,
      value=probe,
      placeholder=placeHolder,
      hxTarget=hxTarget
    ),
    Table(thingRows, theId='searchResults')
  ], theId=theId, attrs={'hx-ext':'morph'})

##########################################################################
# borrowers (post back end)

@pagePart
def searchForABorrower(
  pageData, hxTarget='#level1div', targetUrl='/borrowers/show', **kwargs
) :
  theForm = pageData.form
  nameRows =[]
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
  results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
  linkHyperscript=None
  if len(results) == 1 : linkHyperscript = "init wait 250ms then trigger click on me"
  for aRow in results :
    nameRows.append(TableRow(TableEntry(Link(
      f'{targetUrl}/{aRow['borrowerId']}',
      f'{aRow['firstName']} {aRow['familyName']}',
      hyperscript=linkHyperscript,
      hxTarget=hxTarget
    ))))
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    probe=theForm['search'], thingRows=nameRows,
    theId='level2div', hxPost='/search/borrowers',
    helpName='findBorrower', placeHolder="Type a person's name",
    **kwargs
  )

##########################################################################
# items (aka Books)

@pagePart
def searchForAnItem(
  pageData, hxTarget='#level1div', targetUrl='/itemsInfo/show', **kwargs
) :
  theForm = pageData.form
  itemRows = []
  selectSql = SelectSql(
  ).fields(
    'itemsInfoId', 'title', 'authors'
  ).tables(
    'itemsFTS'
  ).limitTo(10
  ).orderAscBy('rank')
  if theForm['search'] :
    selectSql.whereValue(
      'itemsFTS', theForm['search']+'*', operator='MATCH'
    )
  print(selectSql.sql())
  results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
  linkHyperscript=None
  if len(results) == 1 : linkHyperscript = "init wait 250ms then trigger click on me"
  for aRow in results :
    linkText = aRow['title']
    if aRow['authors'] : linkText += ' ; ' + aRow['authors']
    itemRows.append(TableRow(TableEntry(Link(
      f'{targetUrl}/{aRow['itemsInfoId']}',
      linkText,
      hyperscript=linkHyperscript,
      hxTarget=hxTarget
    ))))
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    probe=theForm['search'], thingRows=itemRows,
    theId='level2div', hxPost='/search/items',
    helpName='findBook', placeHolder='Type a book title...',
    **kwargs
  )
