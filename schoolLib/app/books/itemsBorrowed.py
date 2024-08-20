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
def editItemsBorrowedForm(
  pageData,
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
def getNewItemsBorrowedForm(pageData,
  itemsPhysicalId=None, borrowerId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId :
    return schoolLib.app.books.itemsBorrowed.editItemsBorrowedForm(
      pageData,
      submitMessage='Take out a new book',
      hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
      **kwargs
    )
  return Level0div(
    schoolLib.app.menus.topLevelMenu(pageData)
  )

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  getNewItemsBorrowedForm
)

@pagePart
def postSaveNewItemsBorrowed(pageData,
  itemsPhysicalId=None, borrowersId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowerId :
    theForm = pageData.form
    pageData.db.execute(*InsertSql().sql('itemsBorrowed', {
      'borrowersId'     : borrowersId,
      'itemsPhysicalId' : itemsPhysicalId,
      'dateBorrowed'    : theForm['dateBorrowed'],
      'dateDue'         : theForm['dateDue']
    }))
    pageData.db.commit()
  return Level0div(
    schoolLib.app.menus.topLevelMenu(pageData)
  )

postRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  postSaveNewItemsBorrowed
)

@pagePart
def getEditItemsBorrowedForm(pageData,
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
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsBorrowed :
      return schoolLib.app.books.itemsBorrowed.editItemsBorrowedForm(
        pageData,
        dateBorrowed=itemsBorrowed[0]['dateBorrowed'],
        dateDue=itemsBorrowed[0]['dateDue'],
        submitMessage='Save changes',
        hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/edit/{itemsBorrowedId}',
        **kwargs
      )
  return Level0div(
    schoolLib.app.menus.topLevelMenu(pageData)
  )

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',
  getEditItemsBorrowedForm
)

@pagePart
def putUpdateAnItemsBorrowed(pageData,
  itemsPhysicalId=None, borrowersId=None, itemsBorrowedId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId and itemsBorrowedId :
    theForm = pageData.form
    pageData.db.execute(UpdateSql(
    ).whereValue('id', itemsBorrowedId
    ).whereValue('borrowersId', itemsBorrowersId
    ).whereValue('itemsPhysicalId', itemsPhysicalId
    ).sql('itemsBorrowed', {
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateDue'      : theForm['dateDue']
    }))
    pageData.db.commit()
  return Level0div(
    schoolLib.app.menus.topLevelMenu(pageData)
  )

putRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',
  putUpdateAnItemsBorrowed
)
