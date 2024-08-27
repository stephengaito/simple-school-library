
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
# generic search results HTMX (post back end)

@pagePart
def searchForThings(
  pageData, thingsIterClass,
  targetUrl='/borrowers/show', targetLevel='level1div',
  theId='level2div', hxPost='/search/borrowers', hxTarget=None,
  helpName='findBorrower', placeHolder="Type a person's name",
  **kwargs
) :
  if not hxTarget : hxTarget = '#'+targetLevel
  theForm = pageData.form
  thingsIter = thingsIterClass(targetUrl, theForm, pageData.db)

  linkHyperscript=None
  if thingsIter.numResults == 1 :
    linkHyperscript = "init wait 250ms then trigger click on me"

  thingRows =[]
  for linkUrl, linkText in thingsIter :
    thingRows.append(TableRow(TableEntry(Link(
      linkUrl, linkText,
      level=targetLevel,
      hyperscript=linkHyperscript,
      hxTarget=hxTarget
    ))))
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    probe=theForm['search'], thingRows=thingRows,
    theId=theId, hxPost=hxPost,
    helpName=helpName, placeHolder=placeHolder,
    **kwargs
  )

##########################################################################
# generic iterator (class)

class SearchIter(object) :

  def __init__(self, results, targetUrl) :
    self.results = results
    self.targetUrl = targetUrl
    self.numResults = len(results)
    self.curIter = 0

  def __iter__(self) :
    return self

  def __next__(self) :
    return self.next()

  def nextRow(self) :
    if self.numResults <= self.curIter : raise StopIteration()
    curRow = self.results[self.curIter]
    self.curIter += 1
    return curRow

##########################################################################
# search for a physical item (class)

class SearchForAPhysicalItemIter(SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
    selectSql = SelectSql(
    ).fields(
      'itemsPhysicalId', 'barCode', 'title'
    ).tables('itemsPhysical', 'itemsInfo'
    ).where(

    ).limitTo(10
    ).orderAscBy('barCode')
    if theForm['search'] :
      selectSql.whereValue(
        'barCode', theForm['search']+'%', operator='LIKE'
      )
    print(selectSql.sql())
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    return (
      f'{self.targetUrl}/{curRow['itemsPhysicalId']}',
      f'{curRow['barCode']} {curRow['title']}'
    )
