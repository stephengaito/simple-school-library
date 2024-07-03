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

@get('/classes/new')
def getNewClassForm(request) :
  """
  /classes/new

  GET the HTML Form used to add a new class

  """
  maxClassOrder = 0
  with getDatabase() as db :
    classes = getClasses(db)
    for aClassId, aClass in classes.items() :
      if maxClassOrder < aClass['classOrder'] :
        maxClassOrder = aClass['classOrder']
    maxClassOrder += 1
  return TemplateResponse(request, 'classes/editClassForm.html', {
    'formAction'    : '/classes/new',
    'formMethod'    : 'POST',
    'formSubmitMsg' : 'Add new class',
    'maxClassOrder' : maxClassOrder
  })

@post('/classes/new')
async def postSaveNewClass(request) :
  """
  /classes/new

  Save (POST) the new class as edited by the `getNewClassForm`

  """

  theForm = await request.form()
  with getDatabase() as db :
    db.execute(InsertSql().sql('classes', {
      'name'       : theForm['className'],
      'classOrder' : theForm['classOrder'],
      'desc'       : theForm['classDesc'],
      'colour'     : theForm['classColour']
    }))
    db.commit()
  return GotoResponse('/classes/list')

@get('/classes/edit/{classId:int}')
def getEditAClassForm(request, classId=None) :
  """
  /classes/edit/{classId:int}

  GET the HTML Form used to edit an existing class

  """

  if classId :
    with getDatabase() as db :
      theClasses = getClasses(db)
      if classId in theClasses :
        return TemplateResponse(request, 'classes/editClassForm.html', {
          'formAction'    : f'/classes/edit/{classId}',
          'formMethod'    : 'POST',
          'formSubmitMsg' : 'Save changes',
          'className'     : theClasses[classId]['name'],
          'classOrder'    : theClasses[classId]['classOrder'],
          'classDesc'     : theClasses[classId]['desc'],
          'classColour'   : theClasses[classId]['colour']
        })
  return GotoResponse('/classes/list')

@put('/classes/edit/{classId:int}')
async def putUpdateAClass(request, classId=None) :
  """
  /classes/edit/{classId:int}

  Update (PUT) the details of an existing class as edited by the
  `getEditClassForm`

  """

  theForm = await request.form()
  print("--------------")
  print(classId)
  print(yaml.dump(theForm))
  print("--------------")
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
  return GotoResponse('/')

@delete('/classes/delete/{classId:int}')
def deleteAnEmptyClass(request, classId=None) :
  """
  /classes/delete/{classId:int}

  DELETE an existing class IF AND ONLY IF this class is empty.

  """
  print("DELETE AN EMPTY CLASS")
  with getDatabase() as db :
    selectSql = SelectSql(
    ).fields('id').tables('borrowers'
    ).whereValue('classId', classId)
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    if not results :
      cmd = DeleteSql().whereValue('id', classId).sql('classes')
      print(cmd)
      db.execute(cmd)
      db.commit()
    else :
      print("Can NOT delete a class which is not empty!")
  return GotoResponse('/classes/list')

@get('/classes/list')
def getListOfClassNames(request) :
  """
  /classes/list

  GET the list of existing classes

  """
  with getDatabase() as db :
    theClasses = getClasses(db)
    return TemplateResponse(request, 'classes/listClasses.html', {
      'theClasses' : theClasses,
    })
