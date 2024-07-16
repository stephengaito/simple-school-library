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

  return formTable([
    textInput(
      label='Class name',
      name='className',
      value=className,
      placeholder='A class name...'
    ),
    textInput(
      label='Description',
      name='classDesc',
      value=classDesc,
      placeholder='A description of your class...'
    ),
    numberInput(
      label='Class order',
      name='classOrder',
      value=classOrder,
      defaultValue=0
    ),
    colourInput(
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
  tableRows.append(tableRow([
    tableHeader(text('Name')),
    tableHeader(text('Description')),
    tableHeader(text('Actions'), colspan=3)
  ]))

  with getDatabase() as db :
    theClasses = getClasses(db)
    sortedClasses = getSortedClasses(theClasses)
    for aClass in sortedClasses :
      tableRows.append(tableRow([
        tableEntry(text(aClass['name'])),
        tableEntry(text(aClass['desc'])),
        tableEntry(link(
          f'/classes/list/{aClass['id']}', 'List', target='level1div'
        )),
        tableEntry(link(
          f'/classes/update/{aClass['id']}', 'Update', target='level1div'
        )),
        tableEntry(link(
          f'/classes/edit/{aClass['id']}', 'Edit', target='level1div'
        )),
      ]))

  return table(tableRows, theId='level2div')

def addAClass() :
  maxClassOrder = 0
  with getDatabase() as db :
    classes = getClasses(db)
    for aClassId, aClass in classes.items() :
      if maxClassOrder < aClass['classOrder'] :
        maxClassOrder = aClass['classOrder']
    maxClassOrder += 1

  return level1div([
    menu(secondLevelPeopleMenu, selected='addClass', hxAttrs={
      'hx-target' : '#level1div'
    }),
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
  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='people'),
      addAClass()
    ], theId='level0div')
  )

@get('/menu/people/addClass')
def addAClassMenu(request) :
  return HTMXResponse(
    request,
    addAClass()
  )

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
  return HTMXResponse(request, listClasses())

@get('/classes/edit/{classId:int}')
def getEditAClassForm(request, classId=None) :
  if classId :
    with getDatabase() as db :
      theClasses = getClasses(db)
      if classId in theClasses :
        return HTMXResponse(request, editClassForm(
          className=theClasses[classId]['name'],
          classDesc=theClasses[classId]['desc'],
          classOrder=theClasses[classId]['classOrder'],
          classColour=theClasses[classId]['colour'],
          submitMsg='Save changes',
          postUrl=f'/classes/edit/{classId}'
        ))
  return HTMXResponse(request, listClasses())

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
  return HTMXResponse(request, listClasses())

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
  return HTMXResponse(request, listClasses())
