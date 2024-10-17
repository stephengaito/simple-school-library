"""
Work with itemsPhysical

  - create a new ItemsPhysical
  - edit an itemsPhysical
"""

from datetime import datetime, date
import yaml

from schoolLib.setup import *
from schoolLib.app.books.itemsInfo import editItemsInfoForm
import schoolLib

##########################################################################
# content

today = date.today()

def computeNewBarcode(db) :
  selectSql = SelectSql(
  ).fields('seq'
  ).tables('sqlite_sequence'
  ).whereValue('name', 'itemsPhysical')
  print(selectSql.sql() )
  lastItemsPhysical = selectSql.parseResults(
    db.execute(selectSql.sql()),
    fetchAll=False
  )
  print(yaml.dump(lastItemsPhysical))
  if lastItemsPhysical :
    thisYear = date.today().year
    theSeq = lastItemsPhysical[0]['seq'] + 1
    barcode = "{year}-{seq}".format(
      year=thisYear,
      seq=theSeq
    )
    return barcode
  # a crude but fail-safe choice...
  # This WILL fail if it gets hit more than once per second :$
  return datetime.strftime("%Y-%m%d%H%M%S")

@pagePart
def editItemsPhysicalForm(pageData,
  barcode=None, status=None,
  dateAdded=None, dateBorrowed=None, dateLastSeen=None,
  submitMessage="Save changes", hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- edit itemsPhysical form with NO hxPost -->"

  return FormTable([
    TextInput(
      label='Barcode',
      name='barcode',
      value=barcode,
      placeholder='A barcode...'
    ),
    DateInput(
      label='Date aquired',
      name='dateAdded',
      value=dateAdded,
      placeholder='The date aquired...'
    ),
    DateInput(
      label='Date last borrowed',
      name='dateBorrowed',
      value=dateBorrowed,
      placeholder='The date last borrowed...'
    ),
    DateInput(
      label='Date last seen',
      name='dateLastSeen',
      value=dateLastSeen,
      placeholder='The date last seen...'
    ),
    TextInput(
      label='Status',
      name='status',
      value=status,
      placeholder='The current status...'
    )
  ], submitMsg=submitMessage, hxPost=hxPost, **kwargs)

##########################################################################
# routes

@pagePart
def getNewItemsPhysicalForm(pageData, itemsInfoId=None, **kwargs) :
  if itemsInfoId :
    return schoolLib.app.books.itemsPhysical.editItemsPhysicalForm(
      pageData,
      hxPost=f'/itemsPhysical/{itemsInfoId}/new',
      hxTarget="#level1div",
      submitMessage='Add new copy',
      **kwargs
    )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

getRoute('/itemsPhysical/{itemsInfoId:int}/new', getNewItemsPhysicalForm)

@pagePart
def postSaveNewItemsPhysical(pageData, itemsInfoId=None, **kwargs) :
  if itemsInfoId :
    theForm = pageData.form
    if 'barcode' not in theForm or not theForm['barcode'] :
      barcode = computeNewBarcode(pageData.db)
    else :
      barcode = theForm['barcode']
    pageData.db.execute(*InsertSql().sql('itemsPhysical', {
      'itemsInfoId'  : itemsInfoId,
      'barcode'      : barcode,
      'dateAdded'    : theForm['dateAdded'],
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateLastSeen' : theForm['dateLastSeen'],
      'status'       : theForm['status']
    }))
    pageData.db.commit()
    return schoolLib.app.books.itemsInfo.getShowItemsInfo(
      pageData, itemsInfoId, **kwargs
    )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

postRoute('/itemsPhysical/{itemsInfoId:int}/new', postSaveNewItemsPhysical)

@pagePart
def getEditItemsPhysicalForm(pageData,
  itemsInfoId=None, itemsPhysicalId=None,
  **kwargs
) :
  if itemsInfoId and itemsPhysicalId :
    selectSql = SelectSql().fields(
      'barcode', 'dateAdded', 'dateBorrowed', 'dateLastSeen', 'status'
    ).tables('itemsPhysical'
    ).whereValue('id', itemsPhysicalId
    ).whereValue('itemsInfoId', itemsInfoId)
    itemsPhysical = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsPhysical :
      return schoolLib.app.books.itemsPhysical.editItemsPhysicalForm(
        pageData,
        hxPost=f'/itemsPhysical/{itemsInfoId}/edit/{itemsPhysicalId}',
        barcode=itemsPhysical[0]['barcode'],
        dateAdded=itemsPhysical[0]['dateAdded'],
        dateBorrowed=itemsPhysical[0]['dateBorrowed'],
        dateLastSeen=itemsPhysical[0]['dateLastSeen'],
        status=itemsPhysical[0]['status'],
        submitMessage='Save changes',
        **kwargs
      )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

getRoute(
  '/itemsPhysical/{itemsInfoId:int}/edit/{itemsPhysicalId:int}',
  getEditItemsPhysicalForm
)

@pagePart
def putUpdateAnItemsPhysical(pageData,
  itemsInfoId=None, itemsPhysicalId=None,
  **kwargs
) :
  if itemsInfoId and itemsPhysicalId :
    theForm = pageData.form
    if 'barcode' not in theForm or not theForm['barcode'] :
      barcode = computeNewBarcode(pageData.db)
    else :
      barcode = theForm['barcode']
    pageData.db.execute(UpdateSql(
    ).whereValue('id', itemsPhysicalId
    ).whereValue('itemsInfoId', itemsInfoId
    ).sql('itemsPhysical', {
      'barcode'      : barcode,
      'dateAdded'    : theForm['dateAdded'],
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateLastSeen' : theForm['dateLastSeen'],
      'status'       : theForm['status']
    }))
    pageData.db.commit()
    return schoolLib.app.books.itemsPhysical.editItemsPhysicalForm(
      pageData,
      submitMessage='Add new copy',
      hxPost=f'/itemsPhysical/{itemsInfoId}/new',
      **kwargs
    )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

putRoute(
  '/itemsPhysical/{itemsInfoId:int}/edit/{itemsPhysicalId:int}',
  putUpdateAnItemsPhysical
)

