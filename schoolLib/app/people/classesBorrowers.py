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

def listPupilsInAClassTable(db, classId) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('First name')),
    TableHeader(Text('Family name')),
    TableHeader(Text('Cohort')),
    TableHeader(Text('Class')),
    TableHeader(Text('Actions'))
  ]))
  selectSql = SelectSql(
  ).fields(
    "borrowers.id", "firstName", "familyName", "cohort",
    "classes.name", "classes.colour"
  ).tables(
    "borrowers", "classes"
  ).whereValue("classId", classId
  ).whereField("classId", "classes.id")
  results = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in results :
    tableRows.append(TableRow([
      TableEntry(Text(aRow['firstName'])),
      TableEntry(Text(aRow['familyName'])),
      TableEntry(Text(str(aRow['cohort']))),
      TableEntry(Text(
        addEmojiColour(aRow['classes_colour'], aRow['classes_name'])
      )),
      TableEntry(Button(
        'Edit',
        get=f'/borrowers/edit/{aRow['borrowers_id']}',
        target='#level1div'
      ))
    ]))
  return Table(tableRows, theId='level1div')

def updatePupilsInClassForm(db, classId, postUrl) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('First name')),
    TableHeader(Text('Family name')),
    TableHeader(Text('Cohort')),
    TableHeader(Text('Old class')),
    TableHeader(Text('New class'))
  ]))
  theClasses = getClasses(db, selectedClass=classId)
  sortedClasses = getSortedClasses(theClasses)
  selectSql = SelectSql(
  ).fields(
    "borrowers.id", "firstName", "familyName", "cohort",
    "classes.name", "classes.colour"
  ).tables(
    "borrowers", "classes"
  ).whereValue("classId", classId
  ).whereField("classId", "classes.id")
  results = selectSql.parseResults(db.execute(selectSql.sql()))
  for aRow in results :
    tableRows.append(TableRow([
      TableEntry(Text(aRow['firstName'])),
      TableEntry(Text(aRow['familyName'])),
      TableEntry(Text(str(aRow['cohort']))),
      TableEntry(Text(
        addEmojiColour(aRow['classes_colour'], aRow['classes_name'])
      )),
      TableEntry(ClassesSelector(
        sortedClasses,
        name=f'rowClass-{aRow['borrowers_id']}'
      ))
    ]))
  return FormTable(tableRows, 'Save changes', post=postUrl)

##########################################################################
# routes

@pagePart
def getListPupilsInAClass(request, db, classId=None) :
  if classId :
    return listPupilsInAClassTable(db, classId)
  return listClasses(db)

getRoute('/classes/list/{classId:int}', getListPupilsInAClass)

@pagePart
def getUpdatePupilsInAClassForm(request, db, classId=None) :
  if classId :
    return updatePupilsInClassForm(db, classId, 'classes/update')
  return listClasses(db)

getRoute('/classes/update/{classId:int}', getUpdatePupilsInAClassForm)

@pagePart
async def putUpdatePupilesInAClass(request, db) :
  theForm = await request.form()
  for aKey in theForm.keys() :
    rowClass = theForm[aKey].split('-')
    updateSql = UpdateSql(
    ).whereValue('id', rowClass[1]
    ).whereValue('classId', rowClass[2], operator='!=')
    db.execute(updateSql.sql('borrowers', {
      'classId' : rowClass[2]
    }))
  db.commit()
  return listClasses(db)

putRoute('/classes/update', putUpdatePupilesInAClass)
