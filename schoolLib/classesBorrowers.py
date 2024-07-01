"""
This "module" manages the School Library's work with Classes.

Provide a listing of Borrowers in each class.

    - List the pupils in a given class
    - Reassign the pupils in a give class to a different class
      - This will typically be done once a year before each new
        school year

"""

import sqlite3

from schoolLib.setup import *

@get('/classes/list/{classId:int}')
def getListOfPupilsInAClass(request, classId=None) :
  """
  /classes/list/{classId:int}

  GET the list of Pupils in an existing class

  """

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
  return GotoResponse('/classes/list')

@get('/classes/update/{classId:int}')
def getUpdatePupilsInAClassForm(request, classId=None) :
  """
  /classes/update/{classId:int}

  GET the HTML Form allowing Pupils to be (re)assigned to different
  classes

  """

  if classId :
    classes = getClasses(selectedClass=classId)
    classes = getSortedClasses(classes)
    print(yaml.dump(classes))
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
  return GotoResponse('/classes/list')

@put('/classes/update')
async def putUpdatePupilesInAClass(request) :
  """
  /classes/update

  Update (PUT) the resulting (re)assigned classes for each Pupil as
  edited by the `getUpdatePupilsInAClassForm`

  """

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
