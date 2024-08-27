"""
This "module" manages the collection of borrowers.

"""
import yaml

from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus
import schoolLib.app.people.menu

##########################################################################
# content

@pagePart
def editBorrowerForm(pageData,
  borrowerId=None, submitMessage='Save changes', hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- edit borrower form with NO hxPost -->"

  borrower = {
    'firstName'  : None,
    'familyName' : None,
    'cohort'     : 2020,
    'classId'    : None
  }
  sortedClasses = None
  if borrowerId :
    selectSql = SelectSql(
    ).fields(
      'firstName', 'familyName', 'cohort', 'classId'
    ).tables('borrowers'
    ).whereValue('id', borrowerId)
    borrower = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if borrower :
      sortedClasses = getOrderedClassList(
        pageData.db, selectedClass=borrower[0]['classId']
      )
      borrower = borrower[0]
  if not sortedClasses :
    sortedClasses = getOrderedClassList(pageData.db)

  return FormTable([
    TextInput(
      label="First name",
      name='firstname',
      value=borrower['firstName'],
      placeholder='A first name...'
    ),
    TextInput(
      label="Family name",
      name='familyName',
      value=borrower['familyName'],
      placeholder="A family name..."
    ),
    NumberInput(
      label='Cohort (year entered education)',
      name='cohort',
      value=borrower['cohort'],
    ),
    ClassesSelector(
      sortedClasses,
      label='Class',
      name='assignedClass',
    )
  ], submitMsg="Save changes")


def getBorrowerInfo(db, borrowerId) :

  if not borrowerId : return None

  bSelectSql = SelectSql(
  ).fields(
    'id', 'firstName', 'familyName', 'cohort', 'classId'
  ).tables('borrowers'
  ).whereValue('id', borrowerId)
  borrower = bSelectSql.parseResults(
    db.execute(bSelectSql.sql()),
    fetchAll=False
  )

  if not borrower : return None

  borrower = borrower[0]
  theClasses = getClasses(db)
  borrower['className'] = theClasses[borrower['classId']]['name']
  return (Table([
    TableRow([
      TableEntry(Text('First Name')),
      TableEntry(Text(borrower['firstName'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text('Family Name')),
      TableEntry(Text(borrower['familyName'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text('Cohort')),
      TableEntry(Text(str(borrower['cohort']), klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text('Class')),
      TableEntry(Text(borrower['className'], klass=['bg-yellow-200']))
    ]),
  ], klass=['max-w-prose']), borrower['className'])

def getBorrowerBooksOut(db, borrowerId) :
  ibSelectSql = SelectSql(
  ).fields(
    'itemsInfo.id', 'itemsInfo.title', 'itemsInfo.dewey',
    'itemsPhysical.barCode',
    'itemsBorrowed.dateBorrowed', 'itemsBorrowed.dateDue'
  ).tables(
    'itemsBorrowed', 'itemsPhysical', 'itemsInfo'
  ).whereValue(
    'itemsBorrowed.borrowersId', borrowerId
  ).whereField(
    'itemsPhysical.id', 'itemsBorrowed.itemsPhysicalId'
  ).whereField(
    'itemsInfo.id', 'itemsPhysical.itemsInfoId'
  )
  itemsBorrowed = ibSelectSql.parseResults(
    db.execute(ibSelectSql.sql())
  )
  itemsBorrowedRows = []
  itemsBorrowedRows.append(
    TableRow([
      TableHeader(Text('Title')),
      TableHeader(Text('Barcode')),
      TableHeader(Text('Dewey Decimal Code')),
      TableHeader(Text('Date Borrowed')),
      TableHeader(Text('Date Due')),
    ])
  )
  if itemsBorrowed :
    for anItem in itemsBorrowed :
      itemsBorrowedRows.append(
        TableRow([
          TableEntry(Link(
            f'/itemsInfo/show/{anItem['itemsInfo_id']}',
            anItem['itemsInfo_title'],
            level='level0div',
            hxTarget='#level0div'
          )),
          TableEntry(Link(
            f'/itemsInfo/show/{anItem['itemsInfo_id']}',
            anItem['itemsPhysical_barCode'],
            level='level0div',
            hxTarget='#level0div'
          )),
          TableEntry(Text(anItem['itemsInfo_dewey'])),
          TableEntry(Text(anItem['itemsBorrowed_dateBorrowed'])),
          TableEntry(Text(anItem['itemsBorrowed_dateDue'])),
        ])
      )
  return itemsBorrowedRows

def getBorrowerBooksHistory(db, borrowerId) :
  ibSelectSql = SelectSql(
  ).fields(
    'itemsInfo.id', 'itemsInfo.title', 'itemsInfo.dewey',
    'itemsPhysical.barCode',
    'itemsReturned.dateBorrowed', 'itemsReturned.dateReturned'
  ).tables(
    'itemsReturned', 'itemsPhysical', 'itemsInfo'
  ).whereValue(
    'itemsReturned.borrowersId', borrowerId
  ).whereField(
    'itemsPhysical.id', 'itemsReturned.itemsPhysicalId'
  ).whereField(
    'itemsInfo.id', 'itemsPhysical.itemsInfoId'
  ).orderDescBy('itemsReturned.dateBorrowed')
  itemsReturned = ibSelectSql.parseResults(
    db.execute(ibSelectSql.sql())
  )
  itemsReturnedRows = []
  itemsReturnedRows.append(
    TableRow([
      TableHeader(Text('Title')),
      TableHeader(Text('Barcode')),
      TableHeader(Text('Dewey Decimal Code')),
      TableHeader(Text('Date Borrowed')),
      TableHeader(Text('Date Returned'))
    ])
  )
  if itemsReturned :
    for anItem in itemsReturned :
      itemsReturnedRows.append(
        TableRow([
          TableEntry(Link(
            f'/itemsInfo/show/{anItem['itemsInfo_id']}',
            anItem['itemsInfo_title'],
            level='level0div',
            hxTarget='#level0div'
          )),
          TableEntry(Link(
            f'/itemsInfo/show/{anItem['itemsInfo_id']}',
            anItem['itemsPhysical_barCode'],
            level='level0div',
            hxTarget='#level0div'
          )),
          TableEntry(Text(anItem['itemsInfo_dewey'])),
          TableEntry(Text(anItem['itemsReturned_dateBorrowed'])),
          TableEntry(Text(anItem['itemsReturned_dateReturned'])),
        ])
      )
  return itemsReturnedRows

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

@pagePart
def getShowBorrowerInfo(pageData, borrowerId=None, level=None, **kwargs) :
  print(f"getShowBorrowerInfo: [{level}]")
  borrowerInfo, className = getBorrowerInfo(pageData.db, borrowerId)
  if borrowerInfo :
    itemsBorrowedRows = getBorrowerBooksOut(pageData.db, borrowerId)
    borrowingHistoryRows = getBorrowerBooksHistory(pageData.db, borrowerId)

    if className.lower() != 'staff' and 1 < len(itemsBorrowedRows) :
      takeOutHtmx = Text("Sorry you must return your books before you can take out any more")
    else :
      takeOutHtmx = Text("Take a book out....")
      #takeOutHtmx = Div([
      #  SearchBox(
      #    hxPost='/search/items',
      #    name='search',
      #    helpName='findBook',
      #    value=probe,
      #    placeholder='Type a book title...'
      #  ),
      #  Table(itemRows, theId='searchResults')
      #], attrs={'hx-ext':'morph'})

    theComponent = Level1div([
      schoolLib.app.people.menu.secondLevelSinglePersonMenu(
        pageData, **kwargs
      ),
      borrowerInfo,
      EmptyDiv([]),
      SpacedDiv([]),
      EmptyDiv([]),
      SpacedDiv(takeOutHtmx),
      EmptyDiv([]),
      SpacedDiv([]),
      EmptyDiv([]),
      SpacedDiv([
        RawHtml('<hr/>'),
        Text(
          'Books currently taken out of library',
          klassName='highlight'
        ),
        RawHtml('<hr/>')
      ]),
      EmptyDiv([]),
      Table(itemsBorrowedRows, theId='itemsBorrowed'),
      EmptyDiv([]),
      SpacedDiv([]),
      EmptyDiv([]),
      SpacedDiv([
        RawHtml('<hr/>'),
        Text(
          'Borrowing history',
          klassName='highlight'
        ),
        RawHtml('<hr/>')
      ]),
      EmptyDiv([]),
      Table(borrowingHistoryRows)
    ])
    if level and '0' in level :
      theComponent = Level0div([
        schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
        theComponent
      ])
    return theComponent
  return Level1div([
    schoolLib.app.people.menu.secondLevelPeopleMenu(pageData, selectedId='findBorrower'),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      theId='level2div', hxPost='/search/borrowers',
      helpName='findBorrower', placeHolder="Type a person's name",
      **kwargs
    )

  ])


##########################################################################
# routes

@pagePart
def getNewBorrowerForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='addBorrower'
    ),
    schoolLib.app.people.borrowers.editBorrowerForm(
      pageData,
      submitMsg='Add a new borrower',
      hxPost='/borrowers/new',
      **kwargs
    )
  ])

getRoute('/menu/people/addBorrower', getNewBorrowerForm)

@pagePart
def postSaveNewBorrower(pageData, **kwargs) :
  theForm = pageData.form
  pageData.db.execute(*InsertSql().sql('borrowers', {
    'firstName'  : theForm['firstName'],
    'familyName' : theForm['familyName'],
    'cohort'     : theForm['cohort'],
    'classId'    : theForm['assignedClass']
  }))
  pageData.db.commit()
  return schoolLib.app.people.borrowers.editBorrowerForm(
    pageData,
    submitMsg='Add a new borrower',
    hxPost='/borrowers/new',
    **kwargs
  )

postRoute('/borrowers/new', postSaveNewBorrower)

@pagePart
def getEditABorrowerForm(pageData, borrowerId=None, **kwargs) :
  return schoolLib.app.people.borrowers.editBorrowerForm(
    pageData,
    borrowerId=borrowerId,
    submitMsg= 'Save changes',
    hxPost=f"/borrowers/edit/{borrowerId}",
    **kwargs
  )

getRoute('/borrowers/edit/{borrowerId:int}', getEditABorrowerForm)

@pagePart
def putUpdatedBorrower(pageData, borrowerId=None, **kwargs) :
  if borrowerId :
    theForm = pageData.form
    pageData.db.execute(UpdateSql(
    ).whereValue('id', borrowerId
    ).sql('borrowers', {
      'firstName'  : theForm['firstName'],
      'familyName' : theForm['familyName'],
      'cohort'     : theForm['cohort'],
      'classId'    : theForm['assignedClass']
    }))
    pageData.db.commit()
  return schoolLib.app.people.borrowers.editBorrowerForm(
    pageData,
    submitMsg='Add a new borrower',
    hxPost='/borrowers/new',
    **kwargs
  )

putRoute('/borrowers/edit/{borrowerId:int}', putUpdatedBorrower)

getRoute('/borrowers/show/{borrowerId:int}', getShowBorrowerInfo, anyUser=True)
