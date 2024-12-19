
import yaml
from schoolLib.setup import pagePart, getRoute, SelectSql, postRoute, \
  dbReturnABook, dbTakeOutABook
from schoolLib.htmxComponents import Div, SearchBox, Table, TableRow, \
  TableEntry, Link, Level1div, OobCollection, OobTemplate, TableBody, \
  Text

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
  hxTarget = '#' + theId
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
  ], theId=theId, attrs={'hx-ext': 'morph'})

##########################################################################
# generic search results HTMX (post back end)

@pagePart
def searchForThings(
  pageData, thingsIterClass,
  targetUrl='/borrowers/show', targetLevel='level1div',
  targetSwap='outerHTML', oobLevel=None, search=None,
  theId='level2div', hxPost='/search/borrowers', hxTarget=None,
  helpName='findBorrower', placeHolder="Type a person's name",
  **kwargs
) :
  if not hxTarget : hxTarget = '#' + targetLevel
  theForm = pageData.form

  if search and 'search' not in theForm :
    theForm['search'] = search
  if oobLevel and 'search' in theForm :
    search = theForm['search']

  thingsIter = thingsIterClass(targetUrl, theForm, pageData.db)

  linkHyperscript = None
  if thingsIter.numResults == 1 :
    linkHyperscript = "init wait 250ms then trigger click on me"

  thingRows = []
  for linkUrl, linkText in thingsIter :
    thingRows.append(TableRow(TableEntry(Link(
      linkUrl, linkText,
      level=targetLevel,
      oobLevel=oobLevel,
      search=search,
      hyperscript=linkHyperscript,
      hxTarget=hxTarget,
      hxSwap=targetSwap
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
        'borrowersFTS', theForm['search'] + '*', operator='MATCH'
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
        'itemsFTS', theForm['search'] + '*', operator='MATCH'
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
# search for a borrowed item using a barCode

class SearchForABorrowedItemIter(SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
    selectSql = SelectSql(
    ).fields(
      'itemsBorrowed.id', 'barCode', 'title'
    ).tables('itemsBorrowed', 'itemsPhysical', 'itemsInfo'
    ).whereField(
      'itemsBorrowed.itemsPhysicalId', 'itemsPhysical.id'
    ).whereField(
      'itemsPhysical.itemsInfoId', 'itemsInfo.id'
    ).limitTo(10
    ).orderAscBy('barCode')
    if 'search' in theForm :
      selectSql.whereValue(
        'barCode', theForm['search']  # +'%', operator='LIKE'
      )
    print(selectSql.sql())
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    print(len(results))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    print(yaml.dump(curRow))
    return (
      f'{self.targetUrl}/{curRow['itemsBorrowed_id']}',
      f'{curRow['barCode']} {curRow['title']}'
    )

#########################################
# return a book: from borrower form

"""
@pagePart
def returnABorrowerBookSearch(pageData, hxPost='/borrowers/', **kwargs) :
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    theId='returnABookSearch', hxPost=hxPost,
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

@pagePart
def postReturnABorrowerBookSearch(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, schoolLib.app.utils.finders.SearchForAPhysicalItemIter,
    targetUrl='/borrowers/returnABook', targetLevel=somewhere,
    theId=somewhereElse, hxPost='/search/barCodes',
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

postRoute("/search/barCode/returnBooks", postReturnABorrowerBookSearch, anyUser=True)

@pagePart
def postReturnABook(pageData, borrowerId=None, itemsPhysicalId=None, **kwargs) :
  if not borrowerId or not itemsPhysicalId :
    # do nothing
    if 'headers' not in kwargs : kwargs['headers'] = {}
    kwargs['headers']['HX-Reswap'] = 'none'
    return Div([])

  returnABook( pageData.db, itemsPhysicalId)
  itemsBorrowedRows = getBorrowerBooksOut(db, borrowerId, pageData.user.is_authenticated)
  return Table(itemsBorrowedRows, theId='itemsBorrowed')

postRoute(
  '/borrowers/returnABook/{borrowerId:int}/{itemsPhysicalId:int}',
  postReturnABook, anyUser=True
)
"""  # noqa

#########################################
# return a book: from return a book form

@pagePart
def returnBooksSearch(
  pageData, hxPost='/search/barCode/returnBooks', **kwargs
) :
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    theId='returnABookSearch', hxPost=hxPost,
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

@pagePart
def postReturnBooksSearch(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, schoolLib.app.utils.finders.SearchForABorrowedItemIter,
    targetUrl='/books/returnABook', targetLevel='returnABookSearch',
    oobLevel='booksReturned',
    theId='returnABookSearch', hxPost='/search/barCode/returnBooks',
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

postRoute("/search/barCode/returnBooks", postReturnBooksSearch, anyUser=True)

@pagePart
def getReturnABook(
  pageData, itemsBorrowedId=None,
  level=None, oobLevel=None, search=None,
  **kwargs
) :
  if itemsBorrowedId :
    selectSql = SelectSql(
    ).fields(
      'itemsBorrowed.id', 'barCode', 'title', 'firstName', 'familyName'
    ).tables('itemsBorrowed', 'borrowers', ' itemsPhysical', 'itemsInfo'
    ).whereField(
      'itemsBorrowed.borrowersId', 'borrowers.id'
    ).whereField(
      'itemsBorrowed.itemsPhysicalId', 'itemsPhysical.id'
    ).whereField(
      'itemsPhysical.itemsInfoId', 'itemsInfo.id'
    ).whereValue(
      'itemsBorrowed.id', itemsBorrowedId
    )
    print(selectSql.sql())
    results = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if results :
      results = results[0]
      dbReturnABook(pageData.db, itemsBorrowedId)
      return OobCollection([
        schoolLib.app.utils.finders.searchForThings(
          pageData, schoolLib.app.utils.finders.SearchForABorrowedItemIter,
          targetUrl='/books/returnABook', targetLevel='returnABookSearch',
          oobLevel='booksReturned', search=search,
          theId='returnABookSearch', hxPost='/search/barCode/returnBooks',
          helpName='findBarCode', placeHolder="Type a bar code...",
          **kwargs
        ),
        OobTemplate(
          TableBody([
            TableRow([
              TableEntry(Text(results['barCode'])),
              TableEntry(Text(results['title'])),
              TableEntry(Text(results['firstName'])),
              TableEntry(Text(results['familyName']))
            ]),
          ], hxSwapOob='beforeend:#booksReturned')
        )
      ])

  return Text("hello")

getRoute(
  "/books/returnABook/{itemsBorrowedId:int}", getReturnABook, anyUser=True
)

##########################################################################
# search for a physical item using a barCode

class SearchForAPhysicalItemIter(SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
    selectSql = SelectSql(
    ).fields(
      'itemsPhysical.id', 'barCode', 'title'
    ).tables('itemsPhysical', 'itemsInfo'
    ).whereField(
      'itemsPhysical.itemsInfoId', 'itemsInfo.id'
    ).limitTo(10
    ).orderAscBy('barCode')
    if theForm['search'] :
      selectSql.whereValue(
        'barCode', theForm['search'] + '%', operator='LIKE'
      )
    print(selectSql.sql())
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    return (
      f'{self.targetUrl}/{curRow['itemsPhysical_id']}',
      f'{curRow['barCode']} {curRow['title']}'
    )

#########################################
# Take out a book: from borrower form

@pagePart
def getTakeOutABookSearch(pageData, borrowerId, **kwargs) :
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    theId='takeOutABookSearch',
    hxPost=f"/borrowers/takeOutABookSearch/{borrowerId}",
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

@pagePart
def postTakeOutABookSearch(pageData, borrowerId=None, **kwargs) :
  print("PostTakeOutABookSearch", borrowerId)
  if not borrowerId :
    # do nothing
    if 'headers' not in kwargs : kwargs['headers'] = {}
    kwargs['headers']['HX-Reswap'] = 'none'
    return Div([])

  return schoolLib.app.utils.finders.searchForThings(
    pageData, SearchForAPhysicalItemIter,
    targetUrl=f"/borrowers/takeOutABook/{borrowerId}",
    targetLevel='level1div',
    theId='takeOutABookSearch',
    hxPost=f"/borrowers/takeOutABookSearch/{borrowerId}",
    helpName='findBarCode', placeHolder="Type a bar code...",
    **kwargs
  )

postRoute(
  '/borrowers/takeOutABookSearch/{borrowerId}',
  postTakeOutABookSearch, anyUser=True
)

@pagePart
def getTakeOutABook(
  pageData, borrowerId=None, itemsPhysicalId=None, **kwargs
) :
  print("getTakeOutABook", borrowerId, itemsPhysicalId)
  if not borrowerId or not itemsPhysicalId :
    # do nothing
    if 'headers' not in kwargs : kwargs['headers'] = {}
    kwargs['headers']['HX-Reswap'] = 'none'
    return Div([])

  if dbTakeOutABook(pageData.db, borrowerId, itemsPhysicalId) :
    print("Book taken out")
  else :
    print("Book NOT taken out")
  if 'level' in kwargs : del kwargs['level']
  return schoolLib.app.people.borrowers.getShowBorrowerInfo(
    pageData, borrowerId=borrowerId, level='level1div', **kwargs
  )

getRoute(
  '/borrowers/takeOutABook/{borrowerId:int}/{itemsPhysicalId:int}',
  getTakeOutABook, anyUser=True
)
