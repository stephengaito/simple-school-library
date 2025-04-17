"""
Work with itemsPhysical

  - create a new ItemsPhysical
  - edit an itemsPhysical
"""

from datetime import date
import yaml

from schoolLib.setup import SelectSql, pagePart, getRoute, InsertSql, \
  postRoute, UpdateSql, putRoute
from schoolLib.htmxComponents import FormTable, TextInput, DateInput, Table, \
  TableRow, TableEntry, Text, RefreshMainContent, SpacedDiv, MarkdownDiv
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
  theSeq = 1
  if lastItemsPhysical :
    theSeq = lastItemsPhysical[0]['seq'] + 1

  thisYear = date.today().year
  barcode = "{year}-{seq:04d}".format(
    year=thisYear,
    seq=theSeq
  )
  return barcode

@pagePart
def editItemsPhysicalForm(
  pageData,
  barcode=None, status=None,
  dateAdded=None, dateBorrowed=None, dateLastSeen=None,
  notes=None, location=None,
  submitMessage="Save changes", hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- edit itemsPhysical form with NO hxPost -->"

  if not barcode :  barcode = computeNewBarcode(pageData.db)

  return FormTable([
    TextInput(
      label='Barcode',
      name='barcode',
      value=barcode,
      readOnly=True,
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
    ),
    TextInput(
      label='Notes',
      name='notes',
      value=notes,
      placeholder='Any additional notes...'
    ),
    TextInput(
      label='Location',
      name='location',
      value=location,
      placeholder='The shelf or box location...'
    )
  ], submitMsg=submitMessage, hxPost=hxPost, **kwargs)

def getItemPhysicalTable(db, itemsPhysicalId) :
  if not itemsPhysicalId : return (None, None)

  physicalSelectSql = SelectSql(
  ).fields(
    'itemsInfoId',
    'barCode', 'dateAdded', 'dateBorrowed', 'dateLastSeen',
    'notes', 'status', 'location'
  ).tables(
    'itemsPhysical'
  ).whereValue(
    'id', itemsPhysicalId
  )
  print(physicalSelectSql.sql())
  physicalItem = physicalSelectSql.parseResults(
    db.execute(physicalSelectSql.sql()),
    fetchAll=False
  )
  if not physicalItem : return (None, None)

  physicalItem = physicalItem[0]
  return (Table([
    TableRow([
      TableEntry(Text("Barcode")),
      TableEntry(Text(physicalItem['barCode'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Date Added")),
      TableEntry(Text(physicalItem['dateAdded'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Date Borrowed")),
      TableEntry(Text(physicalItem['dateBorrowed'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Date last seen")),
      TableEntry(Text(physicalItem['dateLastSeen'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Status")),
      TableEntry(Text(physicalItem['status'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Notes")),
      TableEntry(Text(physicalItem['notes'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Location")),
      TableEntry(Text(physicalItem['location'], klass=['bg-yellow-200']))
    ])
  ], klass=['max-w-prose']), physicalItem['itemsInfoId'])

##########################################################################
# routes

@pagePart
def getNewItemsPhysicalForm(pageData, itemsInfoId=None, **kwargs) :
  if itemsInfoId :
    return RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
      schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
      schoolLib.app.books.itemsPhysical.editItemsPhysicalForm(
        pageData,
        hxPost=f'/itemsPhysical/{itemsInfoId}/new',
        submitMessage='Add new copy',
        **kwargs
      )
    )
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(pageData),
    schoolLib.app.books.itemsInfo.editItemsInfoForm(
      pageData,
      submitMessage='Add new book',
      hxPost='/itemsInfo/new',
      **kwargs
    )
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
    selectSql = SelectSql().fields(
      'itemsInfo.id', 'title', 'authors', 'keywords', 'summary',
      'type', 'publisher', 'series'
    ).tables(
      'itemsInfo', 'itemsPhysical'
    ).whereValue(
      'itemsInfo.id', 'itemsInfoId'
    ).whereValue(
      'barCode', barcode
    )
    itemsReturned = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsReturned :
      itemsReturned = itemsReturned[0]
      pageData.db.execute(*InsertSql().sql('itemsFTS', {
        'itemsInfoId'  : itemsInfoId,
        'title'        : itemsReturned['title'],
        'authors'      : itemsReturned['authors'],
        'keywords'     : itemsReturned['keywords'],
        'summary'      : itemsReturned['summary'],
        'type'         : itemsReturned['type'],
        'publisher'    : itemsReturned['publisher'],
        'series'       : itemsReturned['series'],
        'barcode'      : barcode
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
def getEditItemsPhysicalForm(pageData, itemsPhysicalId=None, **kwargs) :
  if itemsPhysicalId :
    selectSql = SelectSql().fields(
      'barcode', 'dateAdded', 'dateBorrowed', 'dateLastSeen',
      'status', 'notes', 'location', 'itemsInfoId'
    ).tables('itemsPhysical'
    ).whereValue('id', itemsPhysicalId)
    itemsPhysical = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsPhysical :
      copyForm = schoolLib.app.books.itemsPhysical.editItemsPhysicalForm(
        pageData,
        hxPost=f'/itemsPhysical/edit/{itemsPhysicalId}',
        barcode=itemsPhysical[0]['barcode'],
        dateAdded=itemsPhysical[0]['dateAdded'],
        dateBorrowed=itemsPhysical[0]['dateBorrowed'],
        dateLastSeen=itemsPhysical[0]['dateLastSeen'],
        status=itemsPhysical[0]['status'],
        notes=itemsPhysical[0]['notes'],
        location=itemsPhysical[0]['location'],
        submitMessage='Save changes',
        **kwargs
      )
      itemsInfoTable = schoolLib.app.books.itemsInfo.getItemInfoTable(
        pageData.db, itemsPhysical[0]['itemsInfoId']
      )
      if itemsInfoTable :
        return RefreshMainContent(
          schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
          schoolLib.app.books.menu.secondLevelSingleBookMenu(
            pageData, **kwargs
          ),
          [
            itemsInfoTable,
            SpacedDiv([]),
            copyForm
          ]
        )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

getRoute(
  '/itemsPhysical/edit/{itemsPhysicalId:int}',
  getEditItemsPhysicalForm
)

@pagePart
def putUpdateAnItemsPhysical(pageData, itemsPhysicalId=None, **kwargs) :
  if itemsPhysicalId :
    theForm = pageData.form
    if 'barcode' not in theForm or not theForm['barcode'] :
      barcode = computeNewBarcode(pageData.db)
    else :
      barcode = theForm['barcode']
    pageData.db.execute(UpdateSql(
    ).whereValue('id', itemsPhysicalId
    ).sql('itemsPhysical', {
      'barcode'      : barcode,
      'dateAdded'    : theForm['dateAdded'],
      'dateBorrowed' : theForm['dateBorrowed'],
      'dateLastSeen' : theForm['dateLastSeen'],
      'status'       : theForm['status']
    }))
    selectSql = SelectSql().fields(
      'itemsInfo.id', 'title', 'authors', 'keywords', 'summary',
      'type', 'publisher', 'series'
    ).tables(
      'itemsInfo', 'itemsPhysical'
    ).whereValue(
      'itemsInfo.id', 'itemsInfoId'
    ).whereValue(
      'barCode', barcode
    )
    itemsReturned = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsReturned :
      itemsReturned = itemsReturned[0]
      pageData.db.execute(*InsertSql().sql('itemsFTS', {
        'itemsInfoId'  : itemsReturned['itemsInfo_id'],
        'title'        : itemsReturned['title'],
        'authors'      : itemsReturned['authors'],
        'keywords'     : itemsReturned['keywords'],
        'summary'      : itemsReturned['summary'],
        'type'         : itemsReturned['type'],
        'publisher'    : itemsReturned['publisher'],
        'series'       : itemsReturned['series'],
        'barcode'      : barcode
      }))
    pageData.db.commit()
    physicalSelectSql = SelectSql(
    ).fields('itemsInfoId'
    ).tables('itemsPhysical'
    ).whereValue('id', itemsPhysicalId)
    print(physicalSelectSql.sql())
    itemsPhysicalData = physicalSelectSql.parseResults(
      pageData.db.execute(physicalSelectSql.sql()),
      fetchAll=False
    )
    if itemsPhysicalData :
      itemsInfoId = itemsPhysicalData[0]['itemsInfoId']
      print(type(itemsInfoId))
      print(itemsInfoId)
      return schoolLib.app.books.itemsInfo.getShowItemsInfo(
        pageData, itemsInfoId, **kwargs
      )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

putRoute(
  '/itemsPhysical/edit/{itemsPhysicalId:int}',
  putUpdateAnItemsPhysical
)

@pagePart
def getItemsPhysicalShow(pageData, itemsPhysicalId=None, **kwargs) :
  physicalCopyTable, itemsInfoId = getItemPhysicalTable(
    pageData.db, itemsPhysicalId
  )
  itemInfoTable = schoolLib.app.books.itemsInfo.getItemInfoTable(
    pageData.db, itemsInfoId
  )
  if itemInfoTable and physicalCopyTable :
    return RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
      schoolLib.app.books.menu.secondLevelSingleBookMenu(
        pageData, **kwargs
      ),
      [
        itemInfoTable,
        SpacedDiv([]),
        physicalCopyTable
      ]
    )
  return schoolLib.app.books.menu.booksMenu(pageData)

getRoute(
  '/itemsPhysical/show/{itemsPhysicalId:int}',
  getItemsPhysicalShow, anyUser=True
)

