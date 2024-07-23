"""
This "module" manages the School Library's work with Classes.

We provide a listing the different classes together with a short
description of each class.

    - Create a new class
    - Edit an existing class
    - Delete an existing class
      - IF this class has no pupils assigned to it
    - List all existing classes

"""

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

def editClassForm(
  className=None, classDesc=None, classOrder=None, classColour=None,
  submitMessage="Save changes", postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- htmx form with NO postUrl -->"

  return FormTable([
    TextInput(
      label='Class name',
      name='className',
      value=className,
      placeholder='A class name...'
    ),
    TextInput(
      label='Description',
      name='classDesc',
      value=classDesc,
      placeholder='A description of your class...'
    ),
    NumberInput(
      label='Class order',
      name='classOrder',
      value=classOrder,
      defaultValue=0
    ),
    ColourInput(
      label='Class colour',
      name='classColour',
      value=classColour,
      defaultValue='#000000'
    )
  ], submitMessage,
    theId='level2div', target='this', post=postUrl, **kwargs
  )

def listClasses(**kwargs) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('Name')),
    TableHeader(Text('Description')),
    TableHeader(Text('Actions'), colspan=4)
  ]))

  with getDatabase() as db :
    theClasses = getClasses(db)
    sortedClasses = getSortedClasses(theClasses)
    for aClass in sortedClasses :
      tableRows.append(TableRow([
        TableEntry(Text(aClass['name'])),
        TableEntry(Text(aClass['desc'])),
        TableEntry(Button(
          'List', get=f'/classes/list/{aClass['id']}', target='#level1div'
        )),
        TableEntry(Button(
          'Update', get=f'/classes/update/{aClass['id']}', target='#level1div'
        )),
        TableEntry(Button(
          'Edit', get=f'/classes/edit/{aClass['id']}', target='#level1div'
        )),
        TableEntry(Button(
          'Delete', get=f'/classes/delete/{aClass['id']}', target='#level1div'
        )),
      ]))

  return Level1div([
    SecondLevelPeopleMenu.select('listClasses'),
    Table(tableRows, theId='level2div')
  ])

def addAClass() :
  maxClassOrder = 0
  with getDatabase() as db :
    classes = getClasses(db)
    for aClassId, aClass in classes.items() :
      if maxClassOrder < aClass['classOrder'] :
        maxClassOrder = aClass['classOrder']
    maxClassOrder += 1

  return Level1div([
    SecondLevelPeopleMenu.select('addClass'),
    editClassForm(
      classOrder=maxClassOrder,
      submitMessage='Add new class',
      postUrl='/classes/new'
    )
  ])

##########################################################################
# routes

@get('/menu/people')
def peopleMenu(request) :
  return Level0div([
    TopLevelMenu.select('people'),
    addAClass()
  ], theId='level0div').response()

@get('/menu/people/addClass')
def addAClassMenu(request) :
  return addAClass().response()

@get('/menu/people/listClasses')
def listClassesMenu(request) :
  return listClasses().response()

@post('/classes/new')
async def postSaveNewClass(request) :
  theForm = await request.form()
  with getDatabase() as db :
    db.execute(InsertSql().sql('classes', {
      'name'       : theForm['className'],
      'classOrder' : theForm['classOrder'],
      'desc'       : theForm['classDesc'],
      'colour'     : theForm['classColour']
    }))
    db.commit()
  return listClasses().response()

@get('/classes/edit/{classId:int}')
def getEditAClassForm(request, classId=None) :
  if classId :
    with getDatabase() as db :
      theClasses = getClasses(db)
      if classId in theClasses :
        return editClassForm(
          className=theClasses[classId]['name'],
          classDesc=theClasses[classId]['desc'],
          classOrder=theClasses[classId]['classOrder'],
          classColour=theClasses[classId]['colour'],
          submitMessage='Save changes',
          postUrl=f'/classes/edit/{classId}'
        ).response()
  return listClasses().response()

@put('/classes/edit/{classId:int}')
async def putUpdateAClass(request, classId=None) :
  theForm = await request.form()
  with getDatabase() as db :
    db.execute(UpdateSql(
    ).whereValue('id', classId
    ).sql('classes', {
      'name'       : theForm['className'],
      'classOrder' : theForm['classOrder'],
      'desc'       : theForm['classDesc'],
      'colour'     : theForm['classColour']
    }))
    db.commit()
  return listClasses().response()

@delete('/classes/delete/{classId:int}')
def deleteAnEmptyClass(request, classId=None) :
  with getDatabase() as db :
    selectSql = SelectSql(
    ).fields('id').tables('borrowers'
    ).whereValue('classId', classId)
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    if not results :
      cmd = DeleteSql().whereValue('id', classId).sql('classes')
      db.execute(cmd)
      db.commit()
    else :
      print("Can NOT delete a class which is not empty!")
  return listClasses().response()
