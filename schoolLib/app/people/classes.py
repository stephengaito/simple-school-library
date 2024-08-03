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

@pagePart
async def editClassForm(request, db,
  className=None, classDesc=None, classOrder=None, classColour=None,
  submitMessage="Save changes", hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- htmx form with NO hxPost -->"

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
    EmojiColourSelector(
      label='Class colour',
      name='classColour',
      selectedColourName=classColour,
    )
  ], submitMessage,
    theId='level2div', hxTarget='this', hxPost=hxPost, **kwargs
  )

@pagePart
async def listClasses(request, db, **kwargs) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('Name')),
    TableHeader(Text('Description')),
    TableHeader(Text('Colour')),
    TableHeader(Text('Actions'), colspan=4)
  ]))

  theClasses = getClasses(db)
  sortedClasses = getSortedClasses(theClasses)
  for aClass in sortedClasses :
    tableRows.append(TableRow([
      TableEntry(Text(aClass['name'])),
      TableEntry(Text(aClass['desc'])),
      TableEntry(Text(addEmojiColour(aClass['colour'],aClass['colour']))),
      TableEntry(Button(
        'List', hxGet=f'/classes/list/{aClass['id']}', hxTarget='#level1div'
      )),
      TableEntry(Button(
        'Update', hxGet=f'/classes/update/{aClass['id']}', hxTarget='#level1div'
      )),
      TableEntry(Button(
        'Edit', hxGet=f'/classes/edit/{aClass['id']}', hxTarget='#level1div'
      )),
      TableEntry(Button(
        'Delete', hxGet=f'/classes/delete/{aClass['id']}', hxTarget='#level1div'
      )),
    ]))

  return Level1div([
    await callPagePart('app.menus.secondLevelPeopleMenu', request, db, selectedId='listClasses'),
    Table(tableRows, theId='level2div')
  ])

@pagePart
async def addAClass(request, db, **kwargs) :
  maxClassOrder = 0
  classes = getClasses(db)
  for aClassId, aClass in classes.items() :
    if maxClassOrder < aClass['classOrder'] :
      maxClassOrder = aClass['classOrder']
  maxClassOrder += 1

  return Level1div([
    await callPagePart('app.menus.secondLevelPeopleMenu', request, db, selectedId='addClass'),
    await callPagePart(
      'app.people.classes.editClassForm',
      request, db,
      classOrder=maxClassOrder,
      submitMessage='Add new class',
      hxPost='/classes/new',
      **kwargs
    )
  ])

##########################################################################
# routes

@pagePart
async def peopleMenu(request, db, **kwargs) :
  return Level0div([
    await callPagePart(
      'app.menus.topLevelMenu', request, db, selectedId='people'
    ),
    await callPagePart(
      'app.people.classes.addAClass', request, db, **kwargs
    )
  ], theId='level0div')

getRoute('/menu/people', peopleMenu)

getRoute('/menu/people/addClass',addAClass)

getRoute('/menu/people/listClasses',listClasses)

@pagePart
async def postSaveNewClass(request, db, **kwargs) :
  theForm = await request.form()
  db.execute(InsertSql().sql('classes', {
    'name'       : theForm['className'],
    'classOrder' : theForm['classOrder'],
    'desc'       : theForm['classDesc'],
    'colour'     : theForm['classColour']
  }))
  db.commit()
  return await callPagePart(
    'app.people.classes.listClasses', request, db, **kwargs
  )

postRoute('/classes/new', postSaveNewClass)

@pagePart
async def getEditAClassForm(request, db, classId=None, **kwargs) :
  if classId :
    theClasses = getClasses(db)
    if classId in theClasses :
      return await callPagePart(
        'app.people.classes.editClassForm',
        request, db,
        className=theClasses[classId]['name'],
        classDesc=theClasses[classId]['desc'],
        classOrder=theClasses[classId]['classOrder'],
        classColour=theClasses[classId]['colour'],
        submitMessage='Save changes',
        hxPost=f'/classes/edit/{classId}',
        **kwargs
      )
  return await callPagePart(
    'app.people.classes.listClasses', request, db, **kwargs
  )

getRoute('/classes/edit/{classId:int}', getEditAClassForm)

@pagePart
async def putUpdateAClass(request, db, classId=None, **kwargs) :
  theForm = await request.form()
  db.execute(UpdateSql(
  ).whereValue('id', classId
  ).sql('classes', {
    'name'       : theForm['className'],
    'classOrder' : theForm['classOrder'],
    'desc'       : theForm['classDesc'],
    'colour'     : theForm['classColour']
  }))
  db.commit()
  return await callPagePart(
    'app.people.classes.listClasses', request, db, **kwargs
  )

putRoute('/classes/edit/{classId:int}', putUpdateAClass)

@pagePart
async def deleteAnEmptyClass(request, db, classId=None, **kwargs) :
  if classId :
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
  return await callPagePart(
    'app.people.classes.listClasses', request, db, **kwargs
  )

deleteRoute('/classes/delete/{classId:int}', deleteAnEmptyClass)
