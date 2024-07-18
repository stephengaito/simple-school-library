
from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

##########################################################################
# content

def booksCheckedOutTableHeader() :
  return tableRow([
    tableHeader(text('Class Name')),
    tableHeader(text("Pupil's Name")),
    tableHeader(text('Title')),
    tableHeader(text('BarCode')),
    tableHeader(text('Date issued')),
    tableHeader(text('Weeks out')),
    tableHeader(text('Date due')),
    tableHeader(text('Days overdue')),
  ])

def booksCheckedOut() :
  bcoRows = []
  bcoRows.append(booksCheckedOutTableHeader())
  with getDatabase() as db :
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
      db.execute(selectSql.sql())
    )
    if booksCheckedOut :
      classes = getClasses(db)
      for aBook in booksCheckedOut :
        bcoRows.append(tableRow([
          tableEntry(text(classes[aBook['borrowers_classId']]['name'])),
          tableEntry(link(
            f'/borrowers/show/{aBook['borrowers_id']}',
            aBook['borrowers_firstName']+' '+aBook['borrowers_familyName'],
            target='#level1div'
          )),
          tableEntry(link(
            f'/books/show/{aBook['itemsInfo_id']}',
            aBook['itemsInfo_title'],
            target='#level1div'
          )),
          tableEntry(text(aBook['itemsPhysical_barcode'])),
          tableEntry(text(aBook['itemsBorrowed_dateBorrowed'])),
          tableEntry(text("")),
          tableEntry(text(aBook['itemsBorrowed_dateDue'])),
          tableEntry(text("")),
        ]))
  return level1div([
    menu(secondLevelTasksMenu, selected='booksCheckedOut'),
    table(bcoRows)
  ])

##########################################################################
# routes

@get('/menu/tasks')
def tasksMenu(request) :
  tasksMarkdown = "somthing about **tasks**"

  return HTMXResponse(
    request,
    level0div([
      menu(topLevelMenu, selected='tasks'),
      booksCheckedOut()
    ], theId='level0div')
  )

@get('/menu/tasks/booksCheckedOut')
def getBooksCheckedOut(request) :
  return HTMXResponse(
    request,
    booksCheckedOut()
  )