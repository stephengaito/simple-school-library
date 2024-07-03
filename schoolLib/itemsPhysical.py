"""
Work with itemsPhysical

  - create a new ItemsPhysical
  - edit an itemsPhysical
"""

from datetime import datetime, date
import yaml

from schoolLib.setup import *

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

@get('/itemsPhysical/{itemsInfoId:int}/new')
def getNewItemsPhysicalForm(request, itemsInfoId=None) :
  """
  /itemsPhysical/{itemsInfoId:int}/new
  """
  if itemsInfoId :
    return TemplateResponse(request, 'items/editItemsPhysicalForm.html', {
      'formAction'    : f'/itemsPhysical/{itemsInfoId}/new',
      'formMethod'    : 'POST',
      'formSubmitMsg' : 'Add new copy',
    })
  return GotoResponse('/')

@post('/itemsPhysical/{itemsInfoId:int}/new')
async def postSaveNewItemsPhysical(request, itemsInfoId=None) :
  if itemsInfoId :
    theForm = await request.form()
    print(yaml.dump(theForm))
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
  return GotoResponse('/')

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
        return TemplateResponse(request, 'items/editItemsPhysicalForm.html', {
          'formAction'    : f'/itemsPhysical/{itemsInfoId}/edit/{itemsPhysicalId}',
          'formMethod'    : 'POST',
          'formSubmitMsg' : 'Save changes',
          'barcode'       : itemsPhysical[0]['barcode'],
          'dateAdded'     : itemsPhysical[0]['dateAdded'],
          'dateBorrowed'  : itemsPhysical[0]['dateBorrowed'],
          'dateLastSeen'  : itemsPhysical[0]['dateLastSeen'],
          'status'        : itemsPhysical[0]['status']
        })
  return GotoResponse('/')

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
  return GotoResponse('/')
