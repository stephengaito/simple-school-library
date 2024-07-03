"""
Work with itemsInfo

    - create a new itemsInfo
    - edit a new itemsInfo

"""

from schoolLib.setup import *

@get('/itemsInfo/new')
def getNewItemsInfoForm(request) :
  """
  /itemsInfo/new
  """
  return TemplateResponse(request, 'items/editItemsInfoForm.html', {
    'formAction'    : '/itemsInfo/new',
    'formMethod'    : 'POST',
    'formSubmitMsg' : 'Add new book',
  })

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
  return GotoResponse('/')

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
        return TemplateResponse(request, 'items/editItemsInfoForm.html', {
          'formAction'    : f'/itemsInfo/edit/{itemsInfoId}',
          'formMethod'    : 'POST',
          'formSubmitMsg' : 'Save changes',
          'title'     : itemsInfo[0]['title'],
          'authors'   : itemsInfo[0]['authors'],
          'publisher' : itemsInfo[0]['publisher'],
          'type'      : itemsInfo[0]['type'],
          'keywords'  : itemsInfo[0]['keywords'],
          'summary'   : itemsInfo[0]['summary'],
          'series'    : itemsInfo[0]['series'],
          'dewey'     : itemsInfo[0]['dewey'],
          'isbn'      : itemsInfo[0]['isbn']

        })
  return GotoResponse('/')

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
  return GotoResponse('/')