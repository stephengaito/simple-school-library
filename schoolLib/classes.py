
import sqlite3

from schoolLib.setup import *

@get('/classes/new')
def newClassForm(request) :
  return TemplateResponse(request, 'classes/newClassForm.html')

@post('/classes/new')
async def saveNewClass(request) :
  print("-------------------------------")
  theForm = await request.form()
  print(yaml.dump(theForm))
  print("-------------------------------")
  return GotoResponse('/')

@get('/classes/list')
def listClasses(request) :
  with getDatabase() as db :
    cursor = db.cursor()
    cursor.execute("SELECT * FROM classes")
    results = cursor.fetchall()
    return TemplateResponse(request, 'classes/listClasses.html', {
      'results' : results,
    })

@get('/classes/list/{classId}')
def listClass(request, classId=None) :
  if classId :
    with getDatabase() as db :
      cursor = db.cursor()
      cursor.execute(f"""
        SELECT firstName, familyName, cohort
        FROM borrowers
        WHERE classId = '{classId}'
      """)
      results = cursor.fetchall()
      return TemplateResponse(request, 'classes/listPupilsInClass.html', {
        'results' : results,
      })
