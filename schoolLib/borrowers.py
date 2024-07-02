"""
This "module" manages the collection of borrowers.

"""

from schoolLib.setup import *

@get('/borrowers/new')
def getNewBorrowerForm(request) :
  """
  /borrowers/new

  GET the HTML form used to add a new borrower
  """

  with getDatabase() as db :
    classes = getOrderedClassList(db)
    return TemplateResponse(request, 'borrowers/editBorrowerForm.html', {
      'action'    : '/borrowers/new',
      'method'    : 'POST',
      'submitMsg' : 'Add a new borrower',
      'classes'   : classes,
      'request'   : request
    })

@post('/borrowers/new')
async def postSaveNewBorrower(request) :
  """
  /borrowers/new

  SAVE (POST) the new borrower as edited by the 'getNewBorrowerForm'
  """

  theForm = await request.form()
  with getDatabase() as db :
    db.execute(InsertSql().sql('borrowers', {
      'firstName'  : theForm['firstName'],
      'familyName' : theForm['familyName'],
      'cohort'     : theForm['cohort'],
      'classId'    : theForm['assignedClass']
    }))
    db.commit()
  return GotoResponse('/')


@get('/borrowers/edit/{borrowerId:int}')
def getEditABorrowerForm(request, borrowerId=None) :
  if borrowerId :
    with getDatabase() as db :
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
        classes = getOrderedClassList(db, selectedClass=borrower[0]['classId'])
        return TemplateResponse(request, 'borrowers/editBorrowerForm.html', {
          'action'    : f"/borrowers/edit/{borrowerId}",
          'submitMsg' : 'Save changes',
          'classes'   : classes,
          'firstName' : borrower[0]['firstName'],
          'familyName': borrower[0]['familyName'],
          'cohort'    : borrower[0]['cohort'],
          'request'   : request,
        })
  return GotoResponse("/")

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
  return GotoResponse("/")
