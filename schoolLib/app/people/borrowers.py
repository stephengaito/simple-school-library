"""
This "module" manages the collection of borrowers.

"""
import yaml

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.finders import *

##########################################################################
# content

def editBorrowerForm(
  borrowerId=None, submitMessage='Save changes', postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- edit borrower form with NO postUrl -->"

  borrower = {
    'firstName'  : None,
    'familyName' : None,
    'cohort'     : 2020,
    'classId'    : None
  }
  with getDatabase() as db :
    sortedClasses = None
    if borrowerId :
      selectSql = SelectSql(
      ).fields(
        'firstName', 'familyName', 'cohort', 'classId'
      ).tables('borrowers'
      ).whereValue('id', borrowerId)
      borrower = selectSql.parseResults(
        db.execute(selectSql.sql()),
        fetchAll=False
      )
      if borrower :
        sortedClasses = getOrderedClassList(db, selectedClass=borrower[0]['classId'])
        borrower = borrower[0]
    if not sortedClasses : sortedClasses = getOrderedClassList(db)

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

@get('/menu/people/addBorrower')
def getNewBorrowerForm(request) :
  return Level1div([
    SecondLevelPeopleMenu.select('addBorrower'),
    editBorrowerForm(
      submitMsg='Add a new borrower',
      postUrl='/borrowers/new'
    )
  ]).response()

@post('/borrowers/new')
async def postSaveNewBorrower(request) :
  theForm = await request.form()
  with getDatabase() as db :
    db.execute(InsertSql().sql('borrowers', {
      'firstName'  : theForm['firstName'],
      'familyName' : theForm['familyName'],
      'cohort'     : theForm['cohort'],
      'classId'    : theForm['assignedClass']
    }))
    db.commit()
  return editBorrowerForm(
    submitMsg='Add a new borrower',
    postUrl='/borrowers/new'
  ).response()

@get('/borrowers/edit/{borrowerId:int}')
def getEditABorrowerForm(request, borrowerId=None) :
  if borrowerId :
    return editBorrowerForm(
      borrowerId=borrowerId,
      submitMsg= 'Save changes',
      postUrl=f"/borrowers/edit/{borrowerId}"
    ).response()
  return editBorrowerForm(
    submitMsg='Add a new borrower',
    postUrl='/borrowers/new'
  ).response()

@put('/borrowers/edit/{borrowerId:int}')
async def putUpdatedBorrower(request, borrowerId=None) :
  if borrowerId :
    theForm = await request.form()
    with getDatabase() as db :
      db.execute(UpdateSql(
      ).whereValue('id', borrowerId
      ).sql('borrowers', {
        'firstName'  : theForm['firstName'],
        'familyName' : theForm['familyName'],
        'cohort'     : theForm['cohort'],
        'classId'    : theForm['assignedClass']
      }))
      db.commit()
  return editBorrowerForm(
    submitMsg='Add a new borrower',
    postUrl='/borrowers/new'
  ).response()

@get('/borrowers/show/{borrowerId:int}')
def getShowBorrowerInfo(request, borrowerId=None) :
  if borrowerId :
    with getDatabase() as db :
      bSelectSql = SelectSql(
      ).fields(
        'id', 'firstName', 'familyName', 'cohort', 'classId'
      ).tables('borrowers'
      ).whereValue('id', borrowerId)
      borrower = bSelectSql.parseResults(
        db.execute(bSelectSql.sql()),
        fetchAll=False
      )
      if borrower :
        borrower = borrower[0]
        theClasses = getClasses(db)
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
          db.execute(ibSelectSql.sql())
        )
        itemsBorrowedRows = []
        itemsBorrowedRows.append(
          TableRow([
            TableHeader('Title'),
            TableHeader('Barcode'),
            TableHeader('Dewey Decimal Code'),
            TableHeader('Date Borrowed'),
            TableHeader('Date Due'),
            TableHeader('Date Returned'),
          ])
        )
        if itemsBorrowed :
          for anItem in itemsBorrowed :
            itemsBorrowedRows.append(
              TableRow([
                TableEntry(Link(
                  f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                  anItem['itemsInfo_title'],
                  target='#level1div'
                )),
                TableEntry(Link(
                  f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                  anItem['itemsPhysical_barCode'],
                  target='#level1div'
                )),
                TableEntry(anItem['itemsInfo_dewey']),
                TableEntry(anItem['itemsBorrowed_dateBorrowed']),
                TableEntry(anItem['itemsBorrowed_dateDue']),
                TableEntry(""),
              ])
            )
        return Level1div([
          Table([
            TableRow([
              TableEntry(text('First Name')),
              TableEntry(text(borrower['firstName']))
            ]),
            TableRow([
              TableEntry(text('Family Name')),
              TableEntry(text(borrower['familyName']))
            ]),
            TableRow([
              TableEntry(text('Cohort')),
              TableEntry(text(str(borrower['cohort'])))
            ]),
            TableRow([
              TableEntry(text('Class')),
              TableEntry(text(borrower['className']))
            ]),
          ]),
          Table(itemsBorrowedRows)
        ]).response()
  return Level1div([
    SecondLevelPeopleMenu.select('findBorrower'),
    findABorrower(None, [])
  ]).response()
