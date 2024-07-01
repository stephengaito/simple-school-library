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

  classes = getOrderedClasses()
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
    cursor = db.cursor()
    cursor.execute("""
      INSERT INTO borrowers (
        firstName, familyName, cohort, classId
      ) VALUES (
        '{firstName}', '{familyName}', '{cohort}', {classId}
      )
    """.format(
      firstName=theForm['firstName'],
      familyName=theForm['familyName'],
      cohort=theForm['cohort'],
      classId=theForm['assignedClass']
    ))
    db.commit()
  return GotoResponse('/')


@get('/borrowers/edit/{borrowerId:int}')
def getEditABorrowerForm(request, borrowerId=None) :
  if borrowerId :
    with getDatabase(asCursor=True) as cursor :
      cursor.execute("""
        SELECT firstName, familyName, cohort, classId
        FROM borrowers
        WHERE id={borrowerId}
      """.format(
        borrowerId=borrowerId
      ))
      borrower = cursor.fetchone()
    if borrower :
      classes = getOrderedClasses(selectedClass=borrower[3])
      return TemplateResponse(request, 'borrowers/editBorrowerForm.html', {
        'action'    : f"/borrowers/edit/{borrowerId}",
        'submitMsg' : 'Save changes',
        'classes'   : classes,
        'firstName' : borrower[0],
        'familyName': borrower[1],
        'cohort'    : borrower[2],
        'request'   : request,
      })
  return GotoResponse("/")

@put('/borrowers/edit/{borrowerId:int}')
async def putUpdatedBorrower(request, borrowerId=None) :
  if borrowerId :
    theForm = await request.form()
    with getDatabase() as db :
      cursor = db.cursor()
      cursor.execute("""
        UPDATE borrowers
        SET
          firstName='{firstName}',
          familyName='{familyName}',
          cohort='{cohort}',
          classId={classId}
        WHERE
          id={borrowerId}
      """.format(
        firstName=theForm['firstName'],
        familyName=theForm['familyName'],
        cohort=theForm['cohort'],
        classId=theForm['assignedClass'],
        borrowerId=borrowerId
      ))
      db.commit()
  return GotoResponse("/")
