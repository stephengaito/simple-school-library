"""
Work with itemsInfo

    - create a new itemsInfo
    - edit a new itemsInfo

"""

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

  return formTable([
    textInput(
      label='Title',
      name='title',
      value=title,
      placeholder='A title...'
    ),
    textInput(
      label='Authors',
      name='authors',
      value=authors,
      placeholder='Some authors...'
    ),
    textInput(
      label='Publisher',
      name='publisher',
      value=publisher,
      placeholder='A publisher...'
    ),
    textInput(
      label='A book type',
      name='type',
      value=bookType,
      placeholder=' A book type...'
    ),
    textAreaInput(
      label='Keywords',
      name='keywords',
      value=keywords,
      placeholder='Some keywords...'
    ),
    textAreaInput(
      label='Summary',
      name='summary',
      value=summary,
      placeholder='A summary...'
    ),
    textInput(
      label='Series',
      name='series',
      value=series,
      placeholder='The series...'
    ),
    textInput(
      label='Dewey decimal classification',
      name='dewey',
      value=dewey,
      placeholder='The dewey decimal classificaton...'
    ),
    textInput(
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

@get('/itemsInfo/new')
def getNewItemsInfoForm(request) :
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

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
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

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
        return HTMXResponse(
          request,
          editItemsInfoForm(
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
          )
        )
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )

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
  return HTMXResponse(
    request,
    editItemsInfoForm(
      submitMessage='Add new book',
      postUrl='/itemsInfo/new',
    )
  )
