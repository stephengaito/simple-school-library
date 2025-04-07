"""
This "module" manages the collection of borrowers.

"""
# import yaml

from schoolLib.setup import pagePart, SelectSql, getOrderedClassList, \
  getClasses, getRoute, InsertSql, postRoute, UpdateSql, putRoute, \
  dbReturnABook
from schoolLib.htmxComponents import FormTable, TextInput, NumberInput, \
  Text, ClassesSelector, Table, TableRow, TableEntry, TableHeader, Link, \
  Div, Button, HelpButton, SpacedDiv, RawHtml, RefreshMainContent
import schoolLib.app.menus
import schoolLib.app.people.menu

##########################################################################
# content

@pagePart
def editBorrowerForm(
  pageData,
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
    ])
  ], klass=['max-w-prose']), borrower['className'])

def getBorrowerBooksOut(db, borrowerId, isAuthenticated=False) :
  ibSelectSql = SelectSql(
  ).fields(
    'itemsInfo.id', 'itemsInfo.title', 'itemsInfo.dewey',
    'itemsPhysical.barCode', 'itemsBorrowed.id',
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
  itemsBorrowedHeader = TableRow([
    TableHeader(Text('Title')),
    TableHeader(Text('Barcode')),
    TableHeader(Text('Dewey Decimal Code')),
    TableHeader(Text('Date Borrowed')),
    TableHeader(Text('Date Due')),
  ])
  if isAuthenticated :
    itemsBorrowedHeader.appendAChild(
      TableHeader(Text('Return')),
    )
  itemsBorrowedRows = []
  itemsBorrowedRows.append(itemsBorrowedHeader)
  if itemsBorrowed :
    for anItem in itemsBorrowed :
      itemsBorrowedRow = TableRow([
        TableEntry(Link(
          f'/itemsInfo/show/{anItem['itemsInfo_id']}',
          anItem['itemsInfo_title'],
        )),
        TableEntry(Link(
          f'/itemsInfo/show/{anItem['itemsInfo_id']}',
          anItem['itemsPhysical_barCode'],
        )),
        TableEntry(Text(anItem['itemsInfo_dewey'])),
        TableEntry(Text(anItem['itemsBorrowed_dateBorrowed'])),
        TableEntry(Text(anItem['itemsBorrowed_dateDue'])),
      ])
      if isAuthenticated :
        itemsBorrowedRow.appendAChild(
          TableEntry(Div([
            Button(
              'Return',
              hxGet=f"/borrowers/returnBook/{borrowerId}/{anItem['itemsBorrowed_id']}",  # noqa
            ),
            HelpButton(hxGet="/help/returnBook/modal")
          ]))
        )
      itemsBorrowedRows.append(itemsBorrowedRow)
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
          )),
          TableEntry(Link(
            f'/itemsInfo/show/{anItem['itemsInfo_id']}',
            anItem['itemsPhysical_barCode'],
          )),
          TableEntry(Text(anItem['itemsInfo_dewey'])),
          TableEntry(Text(anItem['itemsReturned_dateBorrowed'])),
          TableEntry(Text(anItem['itemsReturned_dateReturned'])),
        ])
      )
  return itemsReturnedRows

@pagePart
def getShowBorrowerInfo(pageData, borrowerId=None, level=None, **kwargs) :
  print(f"getShowBorrowerInfo: [{level}]")
  borrowerInfo, className = getBorrowerInfo(pageData.db, borrowerId)
  if borrowerInfo :
    itemsBorrowedRows = getBorrowerBooksOut(
      pageData.db, borrowerId, pageData.user.is_authenticated
    )
    borrowingHistoryRows = getBorrowerBooksHistory(pageData.db, borrowerId)

    if className.lower() != 'staff' and 1 < len(itemsBorrowedRows) :
      takeOutHtmx = Text(
        "Sorry you must return your books before you can take out any more"
      )
    else :
      # takeOutHtmx = Text("search for a book...")
      takeOutHtmx = schoolLib.app.utils.finders.getTakeOutABookSearch(
        pageData, borrowerId, **kwargs
      )

    theComponent = [
      borrowerInfo,
      SpacedDiv([]),
      SpacedDiv([
        RawHtml('<hr/>'),
        Text(
          'Take out a book',
          klassName='highlight'
        ),
        RawHtml('<hr/>')
      ]),
      SpacedDiv(takeOutHtmx),
      SpacedDiv([]),
      SpacedDiv([
        RawHtml('<hr/>'),
        Text(
          'Books currently taken out of library',
          klassName='highlight'
        ),
        RawHtml('<hr/>')
      ]),
      Table(itemsBorrowedRows, theId='itemsBorrowed'),
      SpacedDiv([]),
      SpacedDiv([
        RawHtml('<hr/>'),
        Text(
          'Borrowing history',
          klassName='highlight'
        ),
        RawHtml('<hr/>')
      ]),
      Table(borrowingHistoryRows),
      SpacedDiv([])
    ]
    return RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
      schoolLib.app.people.menu.secondLevelSinglePersonMenu(
        pageData, **kwargs
      ),
      theComponent
    )
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='findBorrower'
    ),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      hxPost='/search/borrowers',
      helpName='findBorrower', placeHolder="Type a person's name",
      **kwargs
    )
  )

##########################################################################
# routes

@pagePart
def getNewBorrowerForm(pageData, **kwargs) :
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='addBorrower'
    ),
    schoolLib.app.people.borrowers.editBorrowerForm(
      pageData,
      submitMsg='Add a new borrower',
      hxPost='/borrowers/new',
      **kwargs
    )
  )

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
  selectSql = SelectSql().fields(
    'borrowers.id'
  ).tables(
    'borrowers'
  ).whereValue(
    'firstName', theForm['firstName']
  ).whereValue(
    'familyName', theForm['familyName']
  )
  itemsReturned = selectSql.parseResults(
    pageData.db.execute(selectSql.sql()),
    fetchAll=False
  )
  if itemsReturned :
    borrowerId = itemsReturned[0]['borrowers_id']
    pageData.db.execute(*InsertSql().sql('borrowersFTS', {
      'borrowerId' : borrowerId,
      'firstName'  : theForm['firstName'],
      'familyName' : theForm['familyName']
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
    pageData.db.execute(UpdateSql(
    ).whereValue('id', borrowerId
    ).sql('borrowersFTS', {
      'firstName'  : theForm['firstName'],
      'familyName' : theForm['familyName']
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

@pagePart
def getBorrowerReturnBook(
  pageData, borrowerId=None, itemsBorrowedId=None, **kwargs
) :
  if itemsBorrowedId : dbReturnABook(pageData.db, itemsBorrowedId)
  kwargs['hxTarget'] = '#mainContent'
  if borrowerId :
    return schoolLib.app.people.borrowers.getShowBorrowerInfo(
      pageData, borrowerId, **kwargs
    )
  return schoolLib.app.people.menu.secondLevelPeopleMenu(
    pageData, selectedId='findBorrower', **kwargs
  )

getRoute(
  '/borrowers/returnBook/{borrowerId:int}/{itemsBorrowedId}',
  getBorrowerReturnBook
)
