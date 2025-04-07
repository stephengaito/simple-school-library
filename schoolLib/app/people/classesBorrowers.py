"""
This "module" manages the School Library's work with Classes.

Provide a listing of Borrowers in each class.

    - List the pupils in a given class
    - Reassign the pupils in a give class to a different class
      - This will typically be done once a year before each new
        school year

"""

from schoolLib.setup          import pagePart, SelectSql, addEmojiColour, \
  getClasses, getSortedClasses, getRoute, UpdateSql, putRoute
from schoolLib.htmxComponents import TableRow, TableHeader, Text, \
  TableEntry, Button, Table, ClassesSelector, FormTable

import schoolLib

##########################################################################
# content

@pagePart
def listPupilsInAClassTable(pageData, classId=None, **kwargs) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('First name')),
    TableHeader(Text('Family name')),
    TableHeader(Text('Cohort')),
    TableHeader(Text('Class')),
    TableHeader(Text('Actions'))
  ]))
  if classId :
    selectSql = SelectSql(
    ).fields(
      "borrowers.id", "firstName", "familyName", "cohort",
      "classes.name", "classes.colour"
    ).tables(
      "borrowers", "classes"
    ).whereValue("classId", classId
    ).whereField("classId", "classes.id")
    results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
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
          hxGet=f'/borrowers/edit/{aRow['borrowers_id']}',
          hxSwap='innerHTML'
        ))
      ]))
  return Table(tableRows)

@pagePart
def updatePupilsInClassForm(pageData, classId=None, hxPost=None, **kwargs) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('First name')),
    TableHeader(Text('Family name')),
    TableHeader(Text('Cohort')),
    TableHeader(Text('Old class')),
    TableHeader(Text('New class'))
  ]))
  if classId and hxPost :
    theClasses = getClasses(pageData.db, selectedClass=classId)
    sortedClasses = getSortedClasses(theClasses)
    selectSql = SelectSql(
    ).fields(
      "borrowers.id", "firstName", "familyName", "cohort",
      "classes.name", "classes.colour"
    ).tables(
      "borrowers", "classes"
    ).whereValue("classId", classId
    ).whereField("classId", "classes.id")
    results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
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
  return FormTable(tableRows, 'Save changes', hxPost=hxPost)

##########################################################################
# routes

getRoute('/classes/list/{classId:int}', listPupilsInAClassTable)

@pagePart
def getUpdatePupilsInAClassForm(pageData, classId=None, **kwargs) :
  return updatePupilsInClassForm(
    pageData,
    classId=classId, hxPost='/classes/update',
    *kwargs
  )

getRoute('/classes/update/{classId:int}', getUpdatePupilsInAClassForm)

@pagePart
def putUpdatePupilesInAClass(pageData, **kwargs) :
  theForm = pageData.form
  for aKey in theForm.keys() :
    rowClass = theForm[aKey].split('-')
    updateSql = UpdateSql(
    ).whereValue('id', rowClass[1]
    ).whereValue('classId', rowClass[2], operator='!=')
    pageData.db.execute(updateSql.sql('borrowers', {
      'classId' : rowClass[2]
    }))
  pageData.db.commit()
  return schoolLib.app.people.classes.listClasses(pageData, **kwargs)

putRoute('/classes/update', putUpdatePupilesInAClass)
