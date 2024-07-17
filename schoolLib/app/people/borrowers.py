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
      #trigger='input changed delay:500ms',
      #target='#level2div',
      #swap='morph:outerHTML',
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
        f'/borrowers/edit/{aRow['borrowerId']}',
        f'{aRow['familyName']}, {aRow['firstName']}',
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
