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

@pagePart
async def editItemsBorrowedForm(
  request, db,
  dateBorrowed=None, dateDue=None,
  submitMessage="Save changes", hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- edit itemsBorrowed form with NO hxPost -->"

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
    theId='level2div', hxTarget='this', hxPost=hxPost, **kwargs
  )

##########################################################################
# routes

@pagePart
async def getNewItemsBorrowedForm(request, db,
  itemsPhysicalId=None, borrowerId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId :
    return await callPagePart(
      'app.books.itemsBorrowed.editItemsBorrowedForm',
      request, db,
      submitMessage='Take out a new book',
      hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
      **kwargs
    )
  return Level0div(
    await callPagePart('app.menus.topLevelMenu', request, db)
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
    await callPagePart('app.menus.topLevelMenu', request, db)
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
      return await callPagePart(
        'app.books.itemsBorrowed.editItemsBorrowedForm',
        request, db,
        dateBorrowed=itemsBorrowed[0]['dateBorrowed'],
        dateDue=itemsBorrowed[0]['dateDue'],
        submitMessage='Save changes',
        hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/edit/{itemsBorrowedId}',
        **kwargs
      )
  return Level0div(
    await callPagePart('app.menus.topLevelMenu', request, db)
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
    await callPagePart('app.menus.topLevelMenu', request, db)
  )

putRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',
  putUpdateAnItemsBorrowed
)
