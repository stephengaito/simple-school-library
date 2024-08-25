
from schoolLib.setup import *
from schoolLib.htmxComponents import *
import schoolLib.app.tasks.menu

##########################################################################
# content

def booksCheckedOutTableHeader() :
  return TableRow([
    TableHeader(Text('Class Name')),
    TableHeader(Text("Pupil's Name")),
    TableHeader(Text('Title')),
    TableHeader(Text('BarCode')),
    TableHeader(Text('Date issued')),
    TableHeader(Text('Weeks out')),
    TableHeader(Text('Date due')),
    TableHeader(Text('Days overdue')),
  ])

@pagePart
def booksCheckedOut(pageData, **kwargs) :
  bcoRows = []
  bcoRows.append(booksCheckedOutTableHeader())
  selectSql = SelectSql(
  ).fields(
    'borrowers.classId', 'borrowers.firstName', 'borrowers.familyName',
    'itemsInfo.title', 'itemsPhysical.barcode',
    'itemsBorrowed.dateBorrowed', 'itemsBorrowed.dateDue',
    'itemsInfo.id', 'borrowers.id'
  ).tables(
    'borrowers', 'itemsBorrowed', 'itemsPhysical', 'itemsInfo'
  ).whereField(
    'borrowers.id', 'itemsBorrowed.borrowersId'
  ).whereField(
    'itemsPhysical.id', 'itemsBorrowed.itemsPhysicalId'
  ).whereField(
    'itemsInfo.id', 'itemsPhysical.itemsInfoId'
  ).groupBy(
    'borrowers.classId', 'itemsBorrowed.dateDue',
    'borrowers.firstName', 'borrowers.familyName'
  )
  #print(selectSql.sql())
  booksCheckedOut = selectSql.parseResults(
    pageData.db.execute(selectSql.sql())
  )
  if booksCheckedOut :
    classes = getClasses(pageData.db)
    for aBook in booksCheckedOut :
      bcoRows.append(TableRow([
        TableEntry(Text(
          addEmojiColour(
            classes[aBook['borrowers_classId']]['colour'],
            classes[aBook['borrowers_classId']]['name']
          )
        )),
        TableEntry(Link(
          f'/borrowers/show/{aBook['borrowers_id']}',
          aBook['borrowers_firstName']+' '+aBook['borrowers_familyName'],
          level='level0div',
          hxTarget='#level0div'
        )),
        TableEntry(Link(
          f'/itemsInfo/show/{aBook['itemsInfo_id']}',
          aBook['itemsInfo_title'],
          level='level0div',
          hxTarget='#level0div'
        )),
        TableEntry(Text(aBook['itemsPhysical_barcode'])),
        TableEntry(Text(aBook['itemsBorrowed_dateBorrowed'])),
        TableEntry(Text("")),
        TableEntry(Text(aBook['itemsBorrowed_dateDue'])),
        TableEntry(Text("")),
      ]))
  return Level1div([
    schoolLib.app.tasks.menu.secondLevelTasksMenu(
      pageData, selectedId='booksCheckedOut'
    ),
    Table(bcoRows)
  ])

##########################################################################
# routes

getRoute('/menu/tasks/booksCheckedOut', booksCheckedOut)