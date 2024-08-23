"""
This "module" manages the collection of borrowers.

"""
import yaml

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.finders import *
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

@pagePart
def getShowBorrowerInfo(pageData, borrowerId=None, **kwargs) :
  if borrowerId :
    bSelectSql = SelectSql(
    ).fields(
      'id', 'firstName', 'familyName', 'cohort', 'classId'
    ).tables('borrowers'
    ).whereValue('id', borrowerId)
    borrower = bSelectSql.parseResults(
      pageData.db.execute(bSelectSql.sql()),
      fetchAll=False
    )
    if borrower :
      borrower = borrower[0]
      theClasses = getClasses(pageData.db)
      borrower['className'] = theClasses[borrower['classId']]['name']
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
        pageData.db.execute(ibSelectSql.sql())
      )
      itemsBorrowedRows = []
      itemsBorrowedRows.append(
        TableRow([
          TableHeader(Text('Title')),
          TableHeader(Text('Barcode')),
          TableHeader(Text('Dewey Decimal Code')),
          TableHeader(Text('Date Borrowed')),
          TableHeader(Text('Date Due')),
          TableHeader(Text('Date Returned'))
        ])
      )
      if itemsBorrowed :
        for anItem in itemsBorrowed :
          itemsBorrowedRows.append(
            TableRow([
              TableEntry(Link(
                f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                anItem['itemsInfo_title'],
                hxTarget='#level1div'
              )),
              TableEntry(Link(
                f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                anItem['itemsPhysical_barCode'],
                hxTarget='#level1div'
              )),
              TableEntry(Text(anItem['itemsInfo_dewey'])),
              TableEntry(Text(anItem['itemsBorrowed_dateBorrowed'])),
              TableEntry(Text(anItem['itemsBorrowed_dateDue'])),
              TableEntry(Text("")),
            ])
          )
      return Level1div([
        schoolLib.app.people.menu.secondLevelSinglePersonMenu(
          pageData, **kwargs
        ),
        Table([
          TableRow([
            TableEntry(Text('First Name')),
            TableEntry(Text(borrower['firstName']))
          ]),
          TableRow([
            TableEntry(Text('Family Name')),
            TableEntry(Text(borrower['familyName']))
          ]),
          TableRow([
            TableEntry(Text('Cohort')),
            TableEntry(Text(str(borrower['cohort'])))
          ]),
          TableRow([
            TableEntry(Text('Class')),
            TableEntry(Text(borrower['className']))
          ]),
        ]),
        EmptyDiv([]),
        SpacedEmptyDiv([]),
        EmptyDiv([]),
        Table(itemsBorrowedRows)
      ])
  return Level1div([
    schoolLib.app.people.menu.secondLevelPeopleMenu(pageData, selectedId='findBorrower'),
    schoolLib.app.finders.findABorrower(pageData, **kwargs)
  ])

getRoute('/borrowers/show/{borrowerId:int}', getShowBorrowerInfo, anyUser=True)
