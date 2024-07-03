"""
Work with itemsBorrowed

  - create a new itemsPhysical
  - edit an itemsPhysical
"""

from schoolLib.setup import *

@get('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new')
def getNewItemsBorrowedForm(request,
  itemsPhysicalId=None, borrowerId=None
) :
  if itemsPhysicalId and borrowersId :
    return TemplateResponse(request, 'items/editItemsBorrowedForm.html', {
      'formAction'    : f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
      'formMethod'    : 'POST',
      'formSubmitMsg' : 'Take out a new book',
    })
  return GotoResponse('/')

@post('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new')
async def postSaveNewItemsBorrowed(request,
  itemsPhysicalId=None, borrowersId=None
) :
  if itemsPhysicalId and borrowerId :
    theForm = await request.form()
    with getDatabase() as db :
      db.execute(InsertSql.().sql('itemsBorrowed', {
        'borrowersId'     : borrowersId,
        'itemsPhysicalId' : itemsPhysicalId,
        'dateBorrowed'    : theForm['dateBorrowed'],
        'dateDue'         : theForm['dateDue']
      }))
      db.commit()
  return GotoResponse('/')

@get('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}')
def getEditItemsBorrowedForm(request,
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
      return TemplateResponse(request, 'items/editItemsBorrowedForm.html', {
        'formAction'    : f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/edit/{itemsBorrowedId}',
        'formMethod'    : 'POST',
        'formSubmitMsg' : 'Save changes',
        'dateBorrowed' : itemsBorrowed[0]['dateBorrowed'],
        'dateDue'      : itemsBorrowed[0]['dateDue']
      })
  return GotoResponse('/')

@put('/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}')
async def putUpdateAnItemsBorrowed(requeset,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None
) :
  if itemsPhysicalId and borrowersId and itemsBorrowedId :
    theForm = await request.form()
    with getDatabase() as db :
      db.execute(UpdateSql(
      ).whereValue('id', itemsBorrowedId
      ).whereValue('borrowersId', itemsBorrowersId
      ).whereValue('itemsPhysicalId', itemsPhysicalId
      ).sql('itemsBorrowed', {
        'dateBorrowed' : theForm['dateBorrowed'],
        'dateDue'      : theForm['dateDue']
      }))
      db.commit()
  return GotoResponse('/')
