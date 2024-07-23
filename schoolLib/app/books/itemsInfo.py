"""
Work with itemsInfo

    - create a new itemsInfo
    - edit a new itemsInfo

"""
import yaml
from schoolLib.setup import *

##########################################################################
# content

def editItemsInfoForm(
  title=None, authors=None, publisher=None, series=None,
  bookType=None, keywords=None, summary=None,
  dewey=None, isbn=None,
  submitMessage="Save changes", postUrl=None,
  **kwargs
) :
  if not postUrl : return "<!-- edit itemsInfo form with NO postUrl -->"

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
    theId='level2div', target='this', post=postUrl, **kwargs
  )

##########################################################################
# routes

@get('/itemsInfo/show/{itemsInfoId:int}')
def getShowItemsInfo(request, itemsInfoId=None) :
  if itemsInfoId :
    with getDatabase() as db :
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
      if itemInfo :
        itemInfo = itemInfo[0]
        physicalSelectSql = SelectSql(
        ).fields(
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
        ).orderBy(
          'barCode'
        )
        print(physicalSelectSql.sql())
        physicalItems = physicalSelectSql.parseResults(
          db.execute(physicalSelectSql.sql())
        )
        physicalItemsRow = []
        physicalItemsRow.append(TableRow([
          TableHeader("Barcode"),
          TableHeader("Date added"),
          TableHeader("Date last seen"),
          TableHeader("Status"),
          TableHeader("Date borrowed"),
          TableHeader("Date due"),
          TableHeader("Borrower"),
          TableHeader("Class")
        ]))
        if physicalItems :
          classes = getClasses(db)
          for aBook in physicalItems :
            print(yaml.dump(aBook))
            borrowerName = ""
            if aBook['borrowers_firstName'] and aBook['borrowers_familyName'] :
              borrowerName = aBook['borrowers_firstName']+' '+aBook['borrowers_familyName']
            borrowerClass = ""
            if aBook['borrowers_classId'] :
              borrowerClass = classes[aBook['borrowers_classId']]['name']
            physicalItemsRow.append(TableRow([
              TableEntry(aBook['itemsPhysical_barCode']),
              TableEntry(aBook['itemsPhysical_dateAdded']),
              TableEntry(aBook['itemsPhysical_dateLastSeen']),
              TableEntry(aBook['itemsPhysical_status']),
              TableEntry(aBook['itemsBorrowed_dateBorrowed']),
              TableEntry(aBook['itemsBorrowed_dateDue']),
              TableEntry(Link(
                f'/borrowers/show/{aBook['borrowers_id']}',
                borrowerName,
                target='#level1div'
              )),
              TableEntry(borrowerClass)
            ]))
        return Level1div([
          Table([
            TableRow([
              TableEntry("Title"),
              TableEntry(itemInfo['title'])
            ]),
            TableRow([
              TableEntry("Authors"),
              TableEntry(itemInfo['authors'])
            ]),
            TableRow([
              TableEntry("Publisher"),
              TableEntry(itemInfo['publisher'])
            ]),
            TableRow([
              TableEntry("Series"),
              TableEntry(itemInfo['series'])
            ]),
            TableRow([
              TableEntry("ISBN"),
              TableEntry(itemInfo['isbn'])
            ]),
            TableRow([
              TableEntry("Dewey Decimal Code"),
              TableEntry(itemInfo['dewey'])
            ]),
            TableRow([
              TtableEntry("Book type"),
              TableEntry(itemInfo['type'])
            ]),
            TableRow([
              TableEntry("Keywords"),
              TableEntry(itemInfo['keywords'])
            ]),
            TableRow([
              TableEntry("Summary"),
              TableEntry(itemInfo['summary'])
            ])
          ]),
          Table(physicalItemsRow)
        ]).response()
  return MarkdownDiv("some thing about itemsInfo").response()

@get('/itemsInfo/new')
def getNewItemsInfoForm(request) :
  return editItemsInfoForm(
    submitMessage='Add new book',
    postUrl='/itemsInfo/new',
  ).response()

@post('/itemsInfo/new')
async def postSaveNewItemsInfo(request) :
  theForm = await request.form()
  with getDatabase() as db :
    db.execute(InsertSql().sql('itemsInfo', {
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
    db.commit()
  return editItemsInfoForm(
    submitMessage='Add new book',
    postUrl='/itemsInfo/new',
  ).response()

@get('/itemsInfo/edit/{itemsInfoId:int}')
def getEditAnItemsInfoForm(request, itemsInfoId=None) :
  if itemsInfoId :
    with getDatabase() as db :
      selectSql = SelectSql().fields(
      'title', 'authors', 'publisher',
      'type',  'keywords', 'summary',
      'series', 'dewey', 'isbn'
      ).tables('itemsInfo'
      ).whereValue('id', itemsInfoId)
      itemsInfo = selectSql.parseResults(
        db.execute(selectSql.sql()),
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
          postUrl=f'/itemsInfo/edit/{itemsInfoId}',
        ).response()
  return editItemsInfoForm(
    submitMessage='Add new book',
    postUrl='/itemsInfo/new',
  ).response()

@put('/itemsInfo/edit/{itemsInfoId:int}')
async def putUpdateAnItemsInfo(request, itemsInfoId=None) :
  if itemsInfoId :
    theForm = await request.form()
    with getDatabase() as db :
      db.execute(UpdateSql(
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
      db.commit()
  return editItemsInfoForm(
    submitMessage='Add new book',
    postUrl='/itemsInfo/new',
  ).response()
