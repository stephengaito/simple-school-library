"""
Work with itemsPhysical

  - create a new ItemsPhysical
  - edit an itemsPhysical
"""

from datetime import datetime, date
import yaml

from schoolLib.setup import *
from schoolLib.app.books.itemsInfo import editItemsInfoForm

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

def editItemsPhysicalForm(
  barcode=None, status=None,
  dateAdded=None, dateBorrowed=None, dateLastSeen=None,
  submitMessage="Save changes", postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- edit itemsPhysical form with NO postUrl -->"

  return formTable([
    textInput(
      label='Barcode',
      name='barcode',
      value=barcode,
      placeholder='A barcode...'
    ),
    dateInput(
      label='Date aquired',
      name='dateAdded',
      value=dateAdded,
      placeholder='The date aquired...'
    ),
    dateInput(
      label='Date last borrowed',
      name='dateBorrowed',
      value=dateBorrowed,
      placeholder='The date last borrowed...'
    ),
    dateInput(
      label='Date last seen',
      name='dateLastSeen',
      value=dateLastSeen,
      placeholder='The date last seen...'
    ),
    textInput(
      label='Status',
      name='status',
      value=status,
      placeholder='The current status...'
    )
  ], submitMessage,
    theId='level2div', target='this', post=postUrl, **kwargs
  )


##########################################################################
# routes

@get('/itemsPhysical/{itemsInfoId:int}/new')
def getNewItemsPhysicalForm(request, itemsInfoId=None) :
  if itemsInfoId :
    return HTMXResponse(
      request,
      editItemsPhysicalForm(
        postUrl=f'/itemsPhysical/{itemsInfoId}/new',
        submitMessage='Add new copy',
      )
    )
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

@post('/itemsPhysical/{itemsInfoId:int}/new')
async def postSaveNewItemsPhysical(request, itemsInfoId=None) :
  if itemsInfoId :
    theForm = await request.form()
    with getDatabase() as db :
      if 'barcode' not in theForm or not theForm['barcode'] :
        barcode = computeNewBarcode(db)
      else :
        barcode = theForm['barcode']
      db.execute(InsertSql().sql('itemsPhysical', {
        'itemsInfoId'  : itemsInfoId,
        'barcode'      : barcode,
        'dateAdded'    : theForm['dateAdded'],
        'dateBorrowed' : theForm['dateBorrowed'],
        'dateLastSeen' : theForm['dateLastSeen'],
        'status'       : theForm['status']
      }))
      db.commit()
    return HTMXResponse(
      request,
      editItemsPhysicalForm(
        submitMessage='Add new copy',
        postUrl=f'/itemsPhysical/{itemsInfoId}/new',
      )
    )
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

@get('/itemsPhysical/{itemsInfoId:int}/edit/{itemsPhysicalId:int}')
def getEditItemsPhysicalForm(request, itemsInfoId=None, itemsPhysicalId=None) :
  if itemsInfoId and itemsPhysicalId :
    with getDatabase() as db :
      selectSql = SelectSql().fields(
        'barcode', 'dateAdded', 'dateBorrowed', 'dateLastSeen', 'status'
      ).tables('itemsPhysical'
      ).whereValue('id', itemsPhysicalId
      ).whereValue('itemsInfoId', itemsInfoId)
      itemsPhysical = selectSql.parseResults(
        db.execute(selectSql.sql()),
        fetchAll=False
      )
      if itemsPhysical :
        return HTMXResponse(
          request,
          editItemsPhysicalForm(
            postUrl=f'/itemsPhysical/{itemsInfoId}/edit/{itemsPhysicalId}',
            barcode=itemsPhysical[0]['barcode'],
            dateAdded=itemsPhysical[0]['dateAdded'],
            dateBorrowed=itemsPhysical[0]['dateBorrowed'],
            dateLastSeen=itemsPhysical[0]['dateLastSeen'],
            status=itemsPhysical[0]['status'],
            submitMessage='Save changes',
          )
        )
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

@put('/itemsPhysical/{itemsInfoId:int}/edit/{itemsPhysicalId:int}')
async def putUpdateAnItemsPhysical(request, itemsInfoId=None, itemsPhysicalId=None) :
  if itemsInfoId and itemsPhysicalId :
    theForm = await request.form()
    with getDatabase() as db :
      if 'barcode' not in theForm or not theForm['barcode'] :
        barcode = computeNewBarcode(db)
      else :
        barcode = theForm['barcode']
      db.execute(UpdateSql(
      ).whereValue('id', itemsPhysicalId
      ).whereValue('itemsInfoId', itemsInfoId
      ).sql('itemsPhysical', {
        'barcode'      : barcode,
        'dateAdded'    : theForm['dateAdded'],
        'dateBorrowed' : theForm['dateBorrowed'],
        'dateLastSeen' : theForm['dateLastSeen'],
        'status'       : theForm['status']
      }))
      db.commit()
    return HTMXResponse(
      request,
      editItemsPhysicalForm(
        submitMessage='Add new copy',
        postUrl=f'/itemsPhysical/{itemsInfoId}/new',
      )
    )
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )
