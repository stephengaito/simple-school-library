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

import sqlite3

from schoolLib.setup import *

@get('/classes/new')
def getNewClassForm(request) :
  """
  /classes/new

  GET the HTML Form used to add a new class

  """
  maxClassOrder = 0
  classes = getClasses()
  for aClassId, aClass in classes.items() :
    if maxClassOrder < aClass['classOrder'] :
      maxClassOrder = aClass['classOrder']
  maxClassOrder += 1
  return TemplateResponse(request, 'classes/editClassForm.html', {
    'action'        : '/classes/new',
    'submitMsg'     : 'Add new class',
    'maxClassOrder' : maxClassOrder
  })

@post('/classes/new')
async def postSaveNewClass(request) :
  """
  /classes/new

  Save (POST) the new class as edited by the `getNewClassForm`

  """

  ## TODO need to protect from `'` used by user.

  theForm = await request.form()
  with getDatabase() as db :
    cursor = db.cursor()
    cursor.execute("""
      INSERT INTO classes (
        name, classOrder, desc, colour
      ) VALUES (
        '{className}', '{classOrder}', '{classDesc}', '{classColour}'
      )
    """.format(
      className=theForm['className'],
      classOrder=theForm['classOrder'],
      classDesc=theForm['classDesc'],
      classColour=theForm['classColour']
    ))
    db.commit()
  return GotoResponse('/classes/list')

@get('/classes/edit/{classId:int}')
def getEditAClassForm(request, classId=None) :
  """
  /classes/edit/{classId:int}

  GET the HTML Form used to edit an existing class

  """

  if classId :
    theClasses = getClasses()
    print("----------------------------")
    print(yaml.dump(theClasses))
    print("----------------------------")
    if classId in theClasses :
      return TemplateResponse(request, 'classes/editClassForm.html', {
        'action'      : f'/classes/edit/{classId}',
        'submitMsg'   : 'Save changes',
        'className'   : theClasses[classId]['name'],
        'classOrder'  : theClasses[classId]['classOrder'],
        'classDesc'   : theClasses[classId]['desc'],
        'classColour' : theClasses[classId]['colour']
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
    cursor = db.cursor()
    cursor.execute("""
      UPDATE classes
      SET
        name='{className}',
        classOrder='{classOrder}',
        desc='{classDesc}',
        colour='{classColour}'
      WHERE
        id={classId}
    """.format(
      classId=classId,
      className=theForm['className'],
      classOrder=theForm['classOrder'],
      classDesc=theForm['classDesc'],
      classColour=theForm['classColour']
    ))
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
    cursor = db.cursor()
    cursor.execute("""
        SELECT id FROM borrowers WHERE classId={classId}
      """.format(classId=classId)
    )
    results = cursor.fetchall()
    print(type(results))
    print(yaml.dump(results))
    if not results :
      cursor.execute("""
          DELETE FROM classes WHERE id={classId}
        """.format(classId=classId)
      )
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

  theClasses = getClasses()
  return TemplateResponse(request, 'classes/listClasses.html', {
    'theClasses' : theClasses,
  })

