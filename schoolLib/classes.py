
import sqlite3

from starlette.responses import PlainTextResponse

from schoolLib.setup import *

@get('/classes/new')
def newClassForm(request) :
  pass

@post('/classes/new')
def newClassDb(request) :
  pass

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
  print(f"Listing class {classId}")
  return PlainTextResponse(f"Listing class {classId}")
