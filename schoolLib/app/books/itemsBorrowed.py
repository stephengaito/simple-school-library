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
    theId='level2div', hxTarget='this', hxPost=postUrl, **kwargs
  )

##########################################################################
# routes

@pagePart
async def getNewItemsBorrowedForm(request, db,
  itemsPhysicalId=None, borrowerId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId :
    return editItemsBorrowedForm(
      submitMessage='Take out a new book',
      postUrl=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
    )
  return Level0div(
      TopLevelMenu
  )

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  getNewItemsBorrowedForm
)

@pagePart
async def postSaveNewItemsBorrowed(request, db,
  itemsPhysicalId=None, borrowersId=None,
  **kwargs
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

postRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  postSaveNewItemsBorrowed
)

@pagePart
async def getEditItemsBorrowedForm(request, db,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None,
  **kwargs
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

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',
  getEditItemsBorrowedForm
)

@pagePart
async def putUpdateAnItemsBorrowed(requeset, db,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None,
  **kwargs
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

putRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',
  putUpdateAnItemsBorrowed
)
