"""
This "module" manages the collection of borrowers.

"""
import yaml

from schoolLib.setup import *

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

  return formTable([
    textInput(
      label="First name",
      name='firstname',
      value=borrower['firstName'],
      placeholder='A first name...'
    ),
    textInput(
      label="Family name",
      name='familyName',
      value=borrower['familyName'],
      placeholder="A family name..."
    ),
    numberInput(
      label='Cohort (year entered education)',
      name='cohort',
      value=borrower['cohort'],
    ),
    classesSelector(
      sortedClasses,
      label='Class',
      name='assignedClass',
    )
  ], submitMsg="Save changes")

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

##########################################################################
# routes

@get('/menu/people/findBorrower')
def getFindBorrowerForm(request) :
  return HTMXResponse(
    request,
    level1div([
      menu(secondLevelPeopleMenu, selected='findBorrower'),
      findABorrower(None, [])
    ])
  )

@get('/menu/people/addBorrower')
def getNewBorrowerForm(request) :
  return HTMXResponse(
    request,
    level1div([
      menu(secondLevelPeopleMenu, selected='addBorrower'),
      editBorrowerForm(
        submitMsg='Add a new borrower',
        postUrl='/borrowers/new'
      )
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
  return HTMXResponse(
    request,
    editBorrowerForm(
      submitMsg='Add a new borrower',
      postUrl='/borrowers/new'
    )
  )

@get('/borrowers/edit/{borrowerId:int}')
def getEditABorrowerForm(request, borrowerId=None) :
  if borrowerId :
    return HTMXResponse(
      request,
      editBorrowerForm(
        borrowerId=borrowerId,
        submitMsg= 'Save changes',
        postUrl=f"/borrowers/edit/{borrowerId}"
      )
    )
  return HTMXResponse(
    request,
    editBorrowerForm(
      submitMsg='Add a new borrower',
      postUrl='/borrowers/new'
    )
  )

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
  return HTMXResponse(
    request,
    editBorrowerForm(
      submitMsg='Add a new borrower',
      postUrl='/borrowers/new'
    )
  )

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
          tableRow([
            tableHeader('Title'),
            tableHeader('Barcode'),
            tableHeader('Dewey Decimal Code'),
            tableHeader('Date Borrowed'),
            tableHeader('Date Due'),
            tableHeader('Date Returned'),
          ])
        )
        if itemsBorrowed :
          for anItem in itemsBorrowed :
            itemsBorrowedRows.append(
              tableRow([
                tableEntry(link(
                  f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                  anItem['itemsInfo_title'],
                  target='#level1div'
                )),
                tableEntry(link(
                  f'/itemsInfo/show/{anItem['itemsInfo_id']}',
                  anItem['itemsPhysical_barCode'],
                  target='#level1div'
                )),
                tableEntry(anItem['itemsInfo_dewey']),
                tableEntry(anItem['itemsBorrowed_dateBorrowed']),
                tableEntry(anItem['itemsBorrowed_dateDue']),
                tableEntry(""),
              ])
            )
        return HTMXResponse(
          request,
          level1div([
            table([
              tableRow([
                tableEntry(text('First Name')),
                tableEntry(text(borrower['firstName']))
              ]),
              tableRow([
                tableEntry(text('Family Name')),
                tableEntry(text(borrower['familyName']))
              ]),
              tableRow([
                tableEntry(text('Cohort')),
                tableEntry(text(str(borrower['cohort'])))
              ]),
              tableRow([
                tableEntry(text('Class')),
                tableEntry(text(borrower['className']))
              ]),
            ]),
            table(itemsBorrowedRows)
          ])
        )
  return HTMXResponse(
    request,
    level1div([
      menu(secondLevelPeopleMenu, selected='findBorrower'),
      findABorrower(None, [])
    ])
  )