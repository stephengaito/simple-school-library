
import sqlite3

from schoolLib.setup import *

@get('/classes/new')
def newClassForm(request) :
  return TemplateResponse(request, 'classes/editClassForm.html', {
    'action'    : '/classes/new'
  })

@post('/classes/new')
async def saveNewClass(request) :
  theForm = await request.form()
  #with getDatabase() as db :
  #  cursor = db.cursor()
  #  cursor.execute("""
  #    INSERT INTO classes ( name ) VALUES ('{className}')
  #  """.format(
  #    className=theForm['className']
  #  ))
  #  db.commit()
  return GotoResponse('/')

@get('/classes/edit/{classId:int}')
def editClassForm(request, classId=None) :
  if classId :
    theClasses = getClasses()
    if 0 <= classId and classId < len(theClasses) :
      return TemplateResponse(request, 'classes/editClassForm.html', {
        'action'    : f'/classes/edit/{classId}',
        'className' : theClasses[classId][1],
        #'classDesc' : theClasses[classId][2]
      })
  return GotoResponse('/classes/list')

@post('/classes/edit/{classId:int}')
async def updateClass(request, classId=None) :
  theForm = await request.form()
  print("--------------")
  print(classId)
  print(yaml.dump(theForm))
  print("--------------")
  with getDatabase() as db :
    cursor = db.cursor()
    cursor.execute("""
      UPDATE classes
      SET name='{className}'
      WHERE id={classId}
    """.format(
      classId=classId,
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

@get('/classes/list/{classId:int}')
def listClass(request, classId=None) :
  if classId :
    results = selectUsing(f"""
      SELECT firstName, familyName, cohort, classes.name
      FROM borrowers, classes
      WHERE classId = {classId}
      AND classId = classes.id
    """)
    return TemplateResponse(request, 'classes/listPupilsInClass.html', {
      'results' : results,
    })
  return GoToResponse('/classes/list')

@get('/classes/update/{classId:int}')
def updateClassForm(request, classId=None) :
  if classId :
    classes = getClasses(selectedClass=classId)
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
