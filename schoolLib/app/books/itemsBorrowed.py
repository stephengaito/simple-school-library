"""
Work with itemsBorrowed

  - create a new itemsPhysical
  - edit an itemsPhysical
"""

from schoolLib.setup import pagePart, getRoute, InsertSql, postRoute, \
  SelectSql, UpdateSql, putRoute
from schoolLib.htmxComponents import FormTable, DateInput, RefreshMainContent
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def editItemsBorrowedForm(
  pageData,
  dateBorrowed=None,
  dateDue=None,
  submitMessage="Save changes",
  hxPost=None,
  **kwargs
) :
  theFormTable = FormTable([
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
    hxTarget='this', hxPost=hxPost, **kwargs
  )
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    theFormTable
  )

##########################################################################
# routes

@pagePart
def getNewItemsBorrowedForm(
  pageData,
  itemsPhysicalId=None,
  borrowersId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId :
    return schoolLib.app.books.itemsBorrowed.editItemsBorrowedForm(
      pageData,
      submitMessage='Take out a new book',
      hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/new',
      **kwargs
    )
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    []
  )

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  getNewItemsBorrowedForm
)

@pagePart
def postSaveNewItemsBorrowed(
  pageData,
  itemsPhysicalId=None,
  borrowersId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId :
    theForm = pageData.form
    pageData.db.execute(*InsertSql().sql('itemsBorrowed', {
      'borrowersId'     : borrowersId,
      'itemsPhysicalId' : itemsPhysicalId,
      'dateBorrowed'    : theForm['dateBorrowed'],
      'dateDue'         : theForm['dateDue']
    }))
    pageData.db.commit()
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    []
  )

postRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/new',
  postSaveNewItemsBorrowed
)

@pagePart
def getEditItemsBorrowedForm(
  pageData,
  itemsPhysicalId=None,
  borrowersId=None,
  itemsBorrowedId=None,
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
        hxPost=f'/itemsBorrowed/{itemsPhysicalId}/{borrowersId}/edit/{itemsBorrowedId}',  # noqa
        **kwargs
      )
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    []
  )

getRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',  # noqa
  getEditItemsBorrowedForm
)

@pagePart
def putUpdateAnItemsBorrowed(
  pageData,
  itemsPhysicalId=None,
  borrowersId=None,
  itemsBorrowedId=None,
  **kwargs
) :
  if itemsPhysicalId and borrowersId and itemsBorrowedId :
    theForm = pageData.form
    pageData.db.execute(UpdateSql(
    ).whereValue('id', itemsBorrowedId
    ).whereValue('borrowersId', borrowersId
    ).whereValue('itemsPhysicalId', itemsPhysicalId
    ).sql('itemsBorrowed', {
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateDue'      : theForm['dateDue']
    }))
    pageData.db.commit()
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    []
  )

putRoute(
  '/itemsBorrowed/{itemsPhysicalId:int}/{borrowersId:int}/edit/{itemsBorrowedId:int}',  # noqa
  putUpdateAnItemsBorrowed
)
