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

from schoolLib.setup import pagePart, getClasses, getSortedClasses,     \
  addEmojiColour, getRoute, InsertSql, postRoute, UpdateSql, putRoute,  \
  SelectSql, DeleteSql, deleteRoute
from schoolLib.htmxComponents import FormTable, TextInput, NumberInput, \
  EmojiColourSelector, TableRow, TableHeader, Text, TableEntry, Div,    \
  Button, HelpButton, RefreshMainContent, Table, getHelpPage
import schoolLib.app.menus
import schoolLib.app.people.menu

##########################################################################
# content

@pagePart
def editClassForm(
  pageData,
  className=None,
  classDesc=None,
  classOrder=None,
  classColour=None,
  submitMessage="Save changes",
  hxPost=None,
  **kwargs
) :
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
    hxTarget='this', hxPost=hxPost, **kwargs
  )

@pagePart
def listClasses(pageData, **kwargs) :
  tableRows = []
  tableRows.append(TableRow([
    TableHeader(Text('Name')),
    TableHeader(Text('Description')),
    TableHeader(Text('Colour')),
    TableHeader(Text('Actions'), colspan=4)
  ]))

  theClasses = getClasses(pageData.db)
  sortedClasses = getSortedClasses(theClasses)
  for aClass in sortedClasses :
    tableRows.append(TableRow([
      TableEntry(Text(aClass['name'])),
      TableEntry(Text(aClass['desc'])),
      TableEntry(Text(addEmojiColour(aClass['colour'], aClass['colour']))),
      TableEntry(Div([
        Button(
          'List', hxGet=f'/classes/list/{aClass['id']}', hxTarget='#content'
        ),
        HelpButton(hxGet="/help/listClass/modal")
      ])),
      TableEntry(Div([
        Button(
          'Update', hxGet=f'/classes/update/{aClass['id']}',
          hxTarget='#content'
        ),
        HelpButton(hxGet="/help/updateClass/modal")
      ])),
      TableEntry(Div([
        Button(
          'Edit', hxGet=f'/classes/edit/{aClass['id']}', hxTarget='#content'
        ),
        HelpButton(hxGet="/help/editClass/modal")
      ])),
      TableEntry(Div([
        Button(
          'Delete', hxGet=f'/classes/delete/{aClass['id']}',
          hxTarget='#content'
        ),
        HelpButton(hxGet="/help/deleteClass/modal")
      ])),
    ]))

  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='listClasses'
    ),
    Table(tableRows)
  )

@pagePart
def addAClass(pageData, **kwargs) :
  maxClassOrder = 0
  classes = getClasses(pageData.db)
  for aClassId, aClass in classes.items() :
    if maxClassOrder < aClass['classOrder'] :
      maxClassOrder = aClass['classOrder']
  maxClassOrder += 1

  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='people'),
    schoolLib.app.people.menu.secondLevelPeopleMenu(
      pageData, selectedId='addClass'
    ),
    [
      schoolLib.app.people.classes.editClassForm(
        pageData,
        classOrder=maxClassOrder,
        submitMessage='Add new class',
        hxPost='/classes/new',
        **kwargs
      ),
      getHelpPage(
        pageData, 'addClass', modal=False,
        klass=['max-w-prose', 'inline-block'],
        hxPost='/editHelp/addClass/nonModal'
      )
    ]
  )

##########################################################################
# routes

getRoute('/menu/people/addClass', addAClass)

getRoute('/menu/people/listClasses', listClasses)

@pagePart
def postSaveNewClass(pageData, **kwargs) :
  theForm = pageData.form
  pageData.db.execute(*InsertSql().sql('classes', {
    'name'       : theForm['className'],
    'classOrder' : theForm['classOrder'],
    'desc'       : theForm['classDesc'],
    'colour'     : theForm['classColour']
  }))
  pageData.db.commit()
  return schoolLib.app.people.classes.listClasses(pageData, **kwargs)

postRoute('/classes/new', postSaveNewClass)

@pagePart
def getEditAClassForm(pageData, classId=None, **kwargs) :
  if classId :
    theClasses = getClasses(pageData.db)
    if classId in theClasses :
      return schoolLib.app.people.classes.editClassForm(
        pageData,
        className=theClasses[classId]['name'],
        classDesc=theClasses[classId]['desc'],
        classOrder=theClasses[classId]['classOrder'],
        classColour=theClasses[classId]['colour'],
        submitMessage='Save changes',
        hxPost=f'/classes/edit/{classId}',
        **kwargs
      )
  return schoolLib.app.people.classes.listClasses(pageData, **kwargs)

getRoute('/classes/edit/{classId:int}', getEditAClassForm)

@pagePart
def putUpdateAClass(pageData, classId=None, **kwargs) :
  theForm = pageData.form
  pageData.db.execute(UpdateSql(
  ).whereValue('id', classId
  ).sql('classes', {
    'name'       : theForm['className'],
    'classOrder' : theForm['classOrder'],
    'desc'       : theForm['classDesc'],
    'colour'     : theForm['classColour']
  }))
  pageData.db.commit()
  return schoolLib.app.people.classes.listClasses(pageData, **kwargs)

putRoute('/classes/edit/{classId:int}', putUpdateAClass)

@pagePart
def deleteAnEmptyClass(pageData, classId=None, **kwargs) :
  if classId :
    selectSql = SelectSql(
    ).fields('id').tables('borrowers'
    ).whereValue('classId', classId)
    results = selectSql.parseResults(pageData.db.execute(selectSql.sql()))
    if not results :
      cmd = DeleteSql().whereValue('id', classId).sql('classes')
      pageData.db.execute(cmd)
      pageData.db.commit()
    else :
      print("Can NOT delete a class which is not empty!")
  return schoolLib.app.people.classes.listClasses(pageData, **kwargs)

deleteRoute('/classes/delete/{classId:int}', deleteAnEmptyClass)
