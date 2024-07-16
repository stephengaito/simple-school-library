"""
This "module" manages the School Library's work with Classes.

Provide a listing of Borrowers in each class.

    - List the pupils in a given class
    - Reassign the pupils in a give class to a different class
      - This will typically be done once a year before each new
        school year

"""

from schoolLib.setup import *

##########################################################################
# content

def listPupilsInAClassTable(classId) :
  tableRows = []
  tableRows.append(tableRow([
    tableHeader(text('First name')),
    tableHeader(text('Family name')),
    tableHeader(text('Cohort')),
    tableHeader(text('Class')),
    tableHeader(text('Actions'))
  ]))
  with getDatabase() as db :
    selectSql = SelectSql(
    ).fields(
      "borrowers.id", "firstName", "familyName", "cohort", "classes.name"
    ).tables(
      "borrowers", "classes"
    ).whereValue("classId", classId
    ).whereField("classId", "classes.id")
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    for aRow in results :
      tableRows.append(tableRow([
        tableEntry(text(aRow['firstName'])),
        tableEntry(text(aRow['familyName'])),
        tableEntry(text(aRow['cohort'])),
        tableEntry(text(aRow['classes_name'])),
        tableEntry(link(f'/borrowers/edit/{ aRow['borrowers_id']}', 'Edit'))
      ]))
  return table(tableRows, theId='level1div')

def updatePupilsInClassForm(classId, postUrl) :
  tableRows = []
  tableRows.append(tableRow([
    tableHeader(text('First name')),
    tableHeader(text('Family name')),
    tableHeader(text('Cohort')),
    tableHeader(text('Old class')),
    tableHeader(text('New class'))
  ]))
  with getDatabase() as db :
    theClasses = getClasses(db)
    sortedClasses = getSortedClasses(theClasses)
    selectSql = SelectSql(
    ).fields(
      "borrowers.id", "firstName", "familyName", "cohort", "classes.name"
    ).tables(
      "borrowers", "classes"
    ).whereValue("classId", classId
    ).whereField("classId", "classes.id")
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    for aRow in results :
      tableRows.append(tableRow([
        tableEntry(text(aRow['firstName'])),
        tableEntry(text(aRow['familyName'])),
        tableEntry(text(aRow['cohort'])),
        tableEntry(text(aRow['classes_name'])),
        tableEntry(classesSelector(
          sortedClasses,
          name=f'rowClass-{aRow['borrowers_id']}'
        ))
      ]))
  return formTable(tableRows, 'Save changes', post=postUrl)

##########################################################################
# routes

@get('/classes/update/{classId:int}')
def getUpdatePupilsInAClassForm(request, classId=None) :
  if classId :
    return HTMXResponse(
      request,
      updatePupilsInClassForm(classId, 'classes/update')
    )
  return HTMXResponse(request, listClasses())

@put('/classes/update')
async def putUpdatePupilesInAClass(request) :
  theForm = await request.form()
  with getDatabase() as db :
    for aKey in theForm.keys() :
      rowClass = theForm[aKey].split('-')
      updateSql = UpdateSql(
      ).whereValue('id', rowClass[1]
      ).whereValue('classId', rowClass[2], operator='!=')
      db.execute(updateSql.sql('borrowers', {
        'classId' : rowClass[2]
      }))
    db.commit()
  return HTMXResponse(request, listClasses())
