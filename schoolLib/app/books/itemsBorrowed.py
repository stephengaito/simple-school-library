"""
Work with itemsBorrowed

  - create a new itemsPhysical
  - edit an itemsPhysical
"""

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

def editItemsBorrowedForm(
  dateBorrowed=None, dateDue=None,
  submitMessage="Save changes", postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- edit itemsBorrowed form with NO postUrl -->"

  return FormTable([
    DateInput(
      label='Date borrowed',
      name='dateBorrowed',
      value=dateBorrowed,
      placeholder='The date last borrowed...'
    ),
    DateInput(
      label='Date due',
      name='dateDue',
      value=dateDue,
      placeholder='The date due....'
    )
  ], submitMessage,
    theId='level2div', target='this', post=postUrl, **kwargs
  )

##########################################################################
# routes

@get('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new')
def getNewItemsBorrowedForm(request, db,
  itemsPhysicalId=None, borrowerId=None
) :
  if itemsPhysicalId and borrowersId :
    return editItemsBorrowedForm(
      submitMessage='Take out a new book',
      postUrl=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
    )
  return Level0div(
      TopLevelMenu
  )

@post('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new')
async def postSaveNewItemsBorrowed(request, db,
  itemsPhysicalId=None, borrowersId=None
) :
  if itemsPhysicalId and borrowerId :
    theForm = await request.form()
    db.execute(InsertSql().sql('itemsBorrowed', {
      'borrowersId'     : borrowersId,
      'itemsPhysicalId' : itemsPhysicalId,
      'dateBorrowed'    : theForm['dateBorrowed'],
      'dateDue'         : theForm['dateDue']
    }))
    db.commit()
  return Level0div(
    TopLevelMenu
  )

@get('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}')
def getEditItemsBorrowedForm(request, db,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None
) :
  if itemsPhysicalId and borrowersId and itemsBorrowedId :
    selectSql = SelectSql(
    ).fields(
      'dateBorrowed', 'dateDue'
    ).tables('itemsBorrowed'
    ).whereValue('id', itemsBorrowedId
    ).whereValue('borrowersId', borrowersId
    ).whereValue('itemsPhysicalId', itemsPhysicalId)
    itemsBorrowed = selectSql.parseResults(
      db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsBorrowed :
      return editItemsBorrowedForm(
        dateBorrowed=itemsBorrowed[0]['dateBorrowed'],
        dateDue=itemsBorrowed[0]['dateDue'],
        submitMessage='Save changes',
        postUrl=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/edit/{itemsBorrowedId}',
      )
  return Level0div(
    TopLevelMenu
  )

@put('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}')
async def putUpdateAnItemsBorrowed(requeset, db,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None
) :
  if itemsPhysicalId and borrowersId and itemsBorrowedId :
    theForm = await request.form()
    db.execute(UpdateSql(
    ).whereValue('id', itemsBorrowedId
    ).whereValue('borrowersId', itemsBorrowersId
    ).whereValue('itemsPhysicalId', itemsPhysicalId
    ).sql('itemsBorrowed', {
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateDue'      : theForm['dateDue']
    }))
    db.commit()
  return Level0div(
    TopLevelMenu
  )
