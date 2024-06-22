
import sqlite3

from schoolLib.setup import *

@get('/classes/new')
def newClassForm(request) :
  return TemplateResponse(request, 'classes/newClassForm.html')

@post('/classes/new')
async def saveNewClass(request) :
  theForm = await request.form()
  with getDatabase() as db :
    cursor = db.cursor()
    cursor.execute("""
      INSERT INTO classes ( name ) VALUES ('{className}')
    """.format(
      className=theForm['className']
    ))
    db.commit()
  return GotoResponse('/')

@get('/classes/list')
def listClasses(request) :
  results = selectUsing("SELECT * FROM classes")
  return TemplateResponse(request, 'classes/listClasses.html', {
    'results' : results,
  })

@get('/classes/list/{classId}')
def listClass(request, classId=None) :
  if classId :
    results = selectUsing(f"""
      SELECT firstName, familyName, cohort, classes.name
      FROM borrowers, classes
      WHERE classId = '{classId}'
      AND classId = classes.id
    """)
    return TemplateResponse(request, 'classes/listPupilsInClass.html', {
      'results' : results,
    })
  return GoToResponse('/classes/list')

@get('/classes/update/{classId}')
def updateClassForm(request, classId=None) :
  if classId :
    classes = getClasses(selectedClass=int(classId))
    results = selectUsing(f"""
      SELECT borrowers.id, firstName, familyName, cohort, classes.name
      FROM borrowers, classes
      WHERE classId = {classId}
      AND   classId = classes.id
    """)
    return TemplateResponse(request, 'classes/updatePupilsInClass.html', {
      'classes' : classes,
      'results' : results
    })
  return GoToResponse('/classes/list')

@post('/classes/update')
async def updateClass(request) :
  theForm = await request.form()
  with getDatabase() as db :
    for aKey in theForm.keys() :
      rowClass = theForm[aKey].split('-')
      cursor = db.cursor()
      cursor.execute("""
        UPDATE borrowers
        SET classId={classId}
        WHERE id={borrowerId}
        AND classId!={classId}
      """.format(
        borrowerId=rowClass[1],
        classId=rowClass[2]
      ))
    db.commit()
  return GotoResponse('/classes/list')
