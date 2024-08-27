
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
# search for a borrower

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

class SearchForABorrowerIter(SearchIter) :
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
def postSearchForBorrower(pageData, level=None, **kwargs) :
  if not level : level = 'level1div'
  print(f"postSearchForBorrower: [{level}]")
  return schoolLib.app.utils.finders.searchForThings(
    pageData, SearchForABorrowerIter,
    targetUrl='/borrowers/show', targetLevel=level,
    theId='level2div', hxPost='/search/borrowers',
    helpName='findBorrower', placeHolder="Type a person's name",
    **kwargs
  )

postRoute('/search/borrowers', postSearchForBorrower, anyUser=True)

##########################################################################
# search for an item

@pagePart
def getFindAnItemForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, selectedId='findBook'
    ),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      theId='level2div', hxPost='/search/items',
      helpName='findBook', placeHolder='Type a book title...',
      **kwargs
    )
  ])

getRoute('/search/items', getFindAnItemForm, anyUser=True)

class SearchForAnItemIter(SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
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
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    linkText = curRow['title']
    if curRow['authors'] : linkText += ' ; ' + curRow['authors']
    return (f'{self.targetUrl}/{curRow['itemsInfoId']}', linkText)

@pagePart
def postSearchForAnItem(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, SearchForAnItemIter,
    targetUrl='/itemsInfo/show', targetLeve='level1div',
    theId='level2div', hxPost='/search/items',
    helpName='findBook', placeHolder='Type a book title...',
    **kwargs
  )

postRoute('/search/items', postSearchForAnItem, anyUser=True)

##########################################################################
# search for a physical item using a barCode

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

@pagePart
def returnABookSearch(pageData, hxPost='/borrowers/', **kwargs) :
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    theId='returnABookSearch', hxPost=hxPost,
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

@pagePart
def postReturnABookSearch(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, schoolLib.app.utils.finders.SearchForAPhysicalItemIter,
    targetUrl='/borrowers/returnABook', targetLevel=somewhere,
    theId=somewhereElse, hxPost='/search/barCodes',
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

#? broken here.... postRoute('')
# here be dragons!

@pagePart
def postReturnABook(pageData, borrowerId=None, itemsPhysicalId=None, **kwargs) :
  if not borrowerId or not itemsPhysicalId :
    # do nothing
    if 'headers' not in kwargs : kwargs['headers'] = {}
    kwargs['headers']['HX-Reswap'] = 'none'
    return Div([])

  returnABook( pageData.db, itemsPhysicalId)
  itemsBorrowedRows = getBorrowerBooksOut(db, borrowerId)
  return Table(itemsBorrowedRows, theId='itemsBorrowed')

postRoute(
  '/borrowers/returnABook/{borrowerId:int}/{itemsPhysicalId:int}',
  postReturnABook, anyUser=True
)

@pagePart
def takeOutABookSearch(pageData, **kwargs) :
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    theId='takeOutABookSearch', hxPost=somewhere,
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

@pagePart
def postTakeOutABook(pageData, borrowerId=None, itemsPhysicalId=None, **kwargs) :
  if not borrowerId or not itemsPhysicalId :
    # do nothing
    if 'headers' not in kwargs : kwargs['headers'] = {}
    kwargs['headers']['HX-Reswap'] = 'none'
    return Div([])

  takeOutABook(pageData.db, borrowerId, itemsPhysicalId)
  itemsBorrowedRows = getBorrowerBooksOut(db, borrowerId)
  return Table(itemsBorrowedRows, theId='itemsBorrowed')

postRoute(
  '/borrowers/takeOutABook/{borrowerId:int}/{barCode:str}',
  postTakeOutABook, anyUser=True
)
