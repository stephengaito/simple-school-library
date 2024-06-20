
import sqlite3

from schoolLib.router import *
from schoolLib.templates import *

@get('/classes/list')
def listClasses(request) :
  with sqlite3.connect('tmp/sslDb.sqlite') as db :
    cursor = db.cursor()
    cursor.execute("SELECT * FROM classes")
    results = cursor.fetchall()
    return TemplateResponse(request, 'classes/listClasses.html', {
      'results' : results,
    })