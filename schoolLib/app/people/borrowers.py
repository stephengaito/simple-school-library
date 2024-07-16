"""
This "module" manages the collection of borrowers.

"""

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
      label='Cohor (year entered education)',
      name='cohort',
      value=borrower['cohort'],
    ),
    classSelector(
      sortedClasses,
      label='Class',
      name='assignedClass',
    )
  ])

##########################################################################
# routes

@get('/borrowers/new')
def getNewBorrowerForm(request) :
  return HTMXResponse(
    request,
    editBorrowerForm(
      submitMsg='Add a new borrower',
      postUrl='/borrowers/new'
    )
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
