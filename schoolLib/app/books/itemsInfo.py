"""
Work with itemsInfo

    - create a new itemsInfo
    - edit a new itemsInfo

"""
import yaml

from schoolLib.setup import pagePart, SelectSql, getClasses, getRoute, \
  InsertSql, postRoute, UpdateSql, putRoute
from schoolLib.htmxComponents import FormTable, TextInput, TextAreaInput, \
  Table, TableRow, TableEntry, Text, TableHeader, Link, \
  Div, Button, HelpButton, MarkdownDiv, RefreshMainContent
import schoolLib.app.books.menu

##########################################################################
# content

@pagePart
def editItemsInfoForm(
  pageData,
  title=None, authors=None, publisher=None, series=None,
  bookType=None, keywords=None, summary=None,
  dewey=None, isbn=None,
  submitMessage="Save changes", hxPost=None,
  **kwargs
) :
  if not hxPost : return "<!-- edit itemsInfo form with NO hxPost -->"

  return FormTable([
    TextInput(
      label='Title',
      name='title',
      value=title,
      placeholder='A title...'
    ),
    TextInput(
      label='Authors',
      name='authors',
      value=authors,
      placeholder='Some authors...'
    ),
    TextInput(
      label='Publisher',
      name='publisher',
      value=publisher,
      placeholder='A publisher...'
    ),
    TextInput(
      label='A book type',
      name='type',
      value=bookType,
      placeholder=' A book type...'
    ),
    TextAreaInput(
      label='Keywords',
      name='keywords',
      value=keywords,
      placeholder='Some keywords...'
    ),
    TextAreaInput(
      label='Summary',
      name='summary',
      value=summary,
      placeholder='A summary...'
    ),
    TextInput(
      label='Series',
      name='series',
      value=series,
      placeholder='The series...'
    ),
    TextInput(
      label='Dewey decimal classification',
      name='dewey',
      value=dewey,
      placeholder='The dewey decimal classificaton...'
    ),
    TextInput(
      label='ISBN',
      name='isbn',
      value=isbn,
      placeholder='The ISBN...'
    )
  ], submitMessage,
    hxTarget='this', hxPost=hxPost, **kwargs
  )

def getItemInfoTable(db, itemsInfoId) :
  if not itemsInfoId : return None

  infoSelectSql = SelectSql(
  ).fields(
    'title', 'authors',
    'publisher', 'series',
    'isbn', 'dewey',
    'type', 'keywords', 'summary'
  ).tables(
    'itemsInfo'
  ).whereValue(
    'id', itemsInfoId
  )
  print(infoSelectSql.sql())
  itemInfo = infoSelectSql.parseResults(
    db.execute(infoSelectSql.sql()),
    fetchAll=False
  )
  if not itemInfo : return None

  itemInfo = itemInfo[0]
  return Table([
    TableRow([
      TableEntry(Text("Title")),
      TableEntry(Text(itemInfo['title'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Authors")),
      TableEntry(Text(itemInfo['authors'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Publisher")),
      TableEntry(Text(itemInfo['publisher'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Series")),
      TableEntry(Text(itemInfo['series'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("ISBN")),
      TableEntry(Text(itemInfo['isbn'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Dewey Decimal Code")),
      TableEntry(Text(itemInfo['dewey'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Book type")),
      TableEntry(Text(itemInfo['type'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Keywords")),
      TableEntry(Text(itemInfo['keywords'], klass=['bg-yellow-200']))
    ]),
    TableRow([
      TableEntry(Text("Summary")),
      TableEntry(Text(itemInfo['summary'], klass=['bg-yellow-200']))
    ])
  ], klass=['max-w-prose'])

def getItemInfoCopiesTable(db, itemsInfoId, isAuthenticated) :
  if not itemsInfoId : return None

  physicalSelectSql = SelectSql(
  ).fields(
    'itemsPhysical.id',
    'itemsPhysical.barCode', 'itemsPhysical.dateAdded',
    'itemsPhysical.dateLastSeen', 'itemsPhysical.status',
    'itemsBorrowed.dateBorrowed', 'itemsBorrowed.dateDue',
    'borrowers.firstName', 'borrowers.familyName',
    'borrowers.classId', 'borrowers.id'
  ).tables(
    'itemsPhysical'
  ).join(
    'itemsBorrowed', 'itemsPhysical.id', 'itemsBorrowed.itemsPhysicalId',
    joinType='LEFT'
  ).join(
    'borrowers', 'borrowers.id', 'itemsBorrowed.borrowersId',
    joinType="LEFT"
  ).whereValue(
    'itemsPhysical.itemsInfoId', itemsInfoId
  ).orderAscBy(
    'barCode'
  )
  print(physicalSelectSql.sql())
  physicalItems = physicalSelectSql.parseResults(
    db.execute(physicalSelectSql.sql())
  )
  physicalItemRows = []
  physicalItemRows.append(TableRow([
    TableHeader(Text("Barcode")),
    TableHeader(Text("Date added")),
    TableHeader(Text("Date last seen")),
    TableHeader(Text("Status")),
    TableHeader(Text("Date borrowed")),
    TableHeader(Text("Date due")),
    TableHeader(Text("Borrower")),
    TableHeader(Text("Class"))
  ]))
  if not physicalItems : return None

  classes = getClasses(db)
  for aBook in physicalItems :
    print(yaml.dump(aBook))
    borrowerName = ""
    if aBook['borrowers_firstName'] and aBook['borrowers_familyName'] :
      borrowerName = aBook['borrowers_firstName'] + ' ' + \
        aBook['borrowers_familyName']
    borrowerClass = ""
    if aBook['borrowers_classId'] :
      borrowerClass = classes[aBook['borrowers_classId']]['name']
    if not aBook['itemsBorrowed_dateBorrowed'] :
      aBook['itemsBorrowed_dateBorrowed'] = ""
    if not aBook['itemsBorrowed_dateDue'] :
      aBook['itemsBorrowed_dateDue'] = ""
    linkAction = "show"
    if isAuthenticated :
      linkAction = "edit"
    physicalItemRows.append(TableRow([
      TableEntry(Link(
        f'/itemsPhysical/{linkAction}/{aBook["itemsPhysical_id"]}',
        aBook['itemsPhysical_barCode']
      )),
      TableEntry(Text(aBook['itemsPhysical_dateAdded'])),
      TableEntry(Text(aBook['itemsPhysical_dateLastSeen'])),
      TableEntry(Text(aBook['itemsPhysical_status'])),
      TableEntry(Text(aBook['itemsBorrowed_dateBorrowed'])),
      TableEntry(Text(aBook['itemsBorrowed_dateDue'])),
      TableEntry(Link(
        f'/borrowers/show/{aBook['borrowers_id']}',
        borrowerName
      )),
      TableEntry(Text(borrowerClass))
    ]))
  return Table(physicalItemRows)

##########################################################################
# routes

@pagePart
def getShowItemsInfo(pageData, itemsInfoId=None, level=None, **kwargs) :
  itemInfoTable       = getItemInfoTable(pageData.db, itemsInfoId)
  itemInfoCopiesTable = getItemInfoCopiesTable(
    pageData.db, itemsInfoId, pageData.user.is_authenticated
  )

  if itemInfoTable and itemInfoCopiesTable :
    theComponent = [
      itemInfoTable,
      itemInfoCopiesTable
    ]

    if pageData.user.is_authenticated :
      theComponent.append(
        Div([
          Button(
            'Add new copy',
            hxGet=f"/itemsPhysical/{itemsInfoId}/new",
            hxTarget="#addPhysicalCopy"
          ),
          HelpButton(hxGet="/help/addCopy/modal")
        ], theId="addPhysicalCopy")
      )
    return RefreshMainContent(
      schoolLib.app.menus.topLevelMenu(
        pageData, selectedId='books'
      ),
      schoolLib.app.books.menu.secondLevelSingleBookMenu(
        pageData, **kwargs
      ),
      theComponent
    )
  return MarkdownDiv("some thing about itemsInfo")

getRoute(
  '/itemsInfo/show/{itemsInfoId:int}',
  getShowItemsInfo, anyUser=True
)

@pagePart
def getNewItemsInfoForm(pageData, **kwargs) :
  return RefreshMainContent(
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, **kwargs
    ),
    editItemsInfoForm(
      pageData,
      submitMessage='Add new book',
      hxPost='/itemsInfo/new',
      **kwargs
    )
  )

getRoute('/itemsInfo/new', getNewItemsInfoForm)

@pagePart
def postSaveNewItemsInfo(pageData, **kwargs):
  theForm = pageData.form
  pageData.db.execute(*InsertSql().sql('itemsInfo', {
    'title'     : theForm['title'],
    'authors'   : theForm['authors'],
    'publisher' : theForm['publisher'],
    'type'      : theForm['type'],
    'keywords'  : theForm['keywords'],
    'summary'   : theForm['summary'],
    'series'    : theForm['series'],
    'dewey'     : theForm['dewey'],
    'isbn'      : theForm['isbn']
  }))
  pageData.db.commit()
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

postRoute('/itemsInfo/new', postSaveNewItemsInfo)

@pagePart
def getEditAnItemsInfoForm(pageData, itemsInfoId=None, **kwargs) :
  if itemsInfoId :
    selectSql = SelectSql().fields(
      'title', 'authors', 'publisher',
      'type',  'keywords', 'summary',
      'series', 'dewey', 'isbn'
    ).tables('itemsInfo'
    ).whereValue('id', itemsInfoId)
    itemsInfo = selectSql.parseResults(
      pageData.db.execute(selectSql.sql()),
      fetchAll=False
    )
    if itemsInfo :
      return editItemsInfoForm(
        title=itemsInfo[0]['title'],
        authors=itemsInfo[0]['authors'],
        publisher=itemsInfo[0]['publisher'],
        bookType=itemsInfo[0]['type'],
        keywords=itemsInfo[0]['keywords'],
        summary=itemsInfo[0]['summary'],
        series=itemsInfo[0]['series'],
        dewey=itemsInfo[0]['dewey'],
        isbn=itemsInfo[0]['isbn'],
        submitMessage='Save changes',
        hxPost=f'/itemsInfo/edit/{itemsInfoId}',
      )
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

getRoute('/itemsInfo/edit/{itemsInfoId:int}', getEditAnItemsInfoForm)

@pagePart
def putUpdateAnItemsInfo(pageData, itemsInfoId=None, **kwargs) :
  if itemsInfoId :
    theForm = pageData.form
    pageData.db.execute(UpdateSql(
    ).whereValue('id', itemsInfoId
    ).sql('itemsInfo', {
      'title'     : theForm['title'],
      'authors'   : theForm['authors'],
      'publisher' : theForm['publisher'],
      'type'      : theForm['type'],
      'keywords'  : theForm['keywords'],
      'summary'   : theForm['summary'],
      'series'    : theForm['series'],
      'dewey'     : theForm['dewey'],
      'isbn'      : theForm['isbn']
    }))
    pageData.db.commit()
  return schoolLib.app.books.itemsInfo.editItemsInfoForm(
    pageData,
    submitMessage='Add new book',
    hxPost='/itemsInfo/new',
    **kwargs
  )

putRoute('/itemsInfo/edit/{itemsInfoId:int}', putUpdateAnItemsInfo)
