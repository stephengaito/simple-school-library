

from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelBooksMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([
    Button(
      'Take a book out of the library',
      theId    = 'takeOut',
      hxGet    = '/menu/books/takeOut',
      hxTarget = '#level1div'
    ),
    Button(
      'Return books to the library',
      theId    = 'return',
      hxGet    = '/menu/books/return',
      hxTarget = '#level1div'
    ),
    Button(
      'Find a book',
      theId    = 'findBook',
      hxGet    = '/search/items',
      hxTarget = '#level1div'
    )
  ], selectedId=selectedId, klassName='vertical')

  if pageData.user.is_authenticated :
    theMenu.appendAChild(
      Button(
        'Add a book',
        theId    = 'addBook',
        hxGet    = '/itemsInfo/new',
        hxTarget = '#level1div'
      )
    )
  return theMenu

@pagePart
def secondLevelSingleBookMenu(pageData, selectedId=None, **kwargs) :
  theMenu = Menu([], klassName='vertical')

  # edit itemInfo
  # delete book (only if no copies)
  # add a copy

  if pageData.user.is_authenticated :
    pass

  if selectedId : theMenu.select(selectedId)
  return theMenu

@pagePart
def booksMenu(pageData, **kwargs) :

  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='books'),
    Level1div([
      secondLevelBooksMenu(pageData),
      getHelpPage(
        pageData, 'booksPage', modal=False,
        hxPost='/editHelp/booksPage/nonModal'
      )
    ])
  ])

##########################################################################
# routes

getRoute('/menu/books', booksMenu, anyUser=True)

@pagePart
def getFindAnItemForm(pageData, **kwargs) :
  return Level1div([
    schoolLib.app.books.menu.secondLevelBooksMenu(
      pageData, selectedId='findBook'
    ),
    schoolLib.app.utils.finders.findAThing(
      pageData,
      theId='level2div', hxPost='/search/items',
      helpName='findBook', placeHolder='Type a book title...',
      **kwargs
    )
  ])

getRoute('/search/items', getFindAnItemForm, anyUser=True)

class SearchForAnItemIter(schoolLib.app.utils.finders.SearchIter) :
  def __init__(self, targetUrl, theForm, db) :
    selectSql = SelectSql(
    ).fields(
      'itemsInfoId', 'title', 'authors'
    ).tables(
      'itemsFTS'
    ).limitTo(10
    ).orderAscBy('rank')
    if theForm['search'] :
      selectSql.whereValue(
        'itemsFTS', theForm['search']+'*', operator='MATCH'
      )
    print(selectSql.sql())
    results = selectSql.parseResults(db.execute(selectSql.sql()))
    super().__init__(results, targetUrl)

  def next(self) :
    curRow = self.nextRow()
    linkText = curRow['title']
    if curRow['authors'] : linkText += ' ; ' + curRow['authors']
    return (f'{self.targetUrl}/{curRow['itemsInfoId']}', linkText)

@pagePart
def postSearchForAnItem(pageData, **kwargs) :
  return schoolLib.app.utils.finders.searchForThings(
    pageData, SearchForAnItemIter,
    hxTarget='#level1div', targetUrl='/itemsInfo/show',
    theId='level2div', hxPost='/search/items',
    helpName='findBook', placeHolder='Type a book title...',
    **kwargs
  )

postRoute('/search/items', postSearchForAnItem, anyUser=True)
