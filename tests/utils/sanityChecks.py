
# import glob
import os
import re
import sys
import yaml

from schoolLib.app.main import setupApp
from schoolLib.setup.router import pageParts, \
  computePagePartUsers, routes

def sanitizeUrl(hxUrl) :
  """
  Check that all hxGet and hxPost URLs have a corresponding route.
  """
  hxUrl = hxUrl.strip('f\"\')')
  hxPrefix = hxUrl
  if 'editHelp' in hxPrefix :
    hxPrefix = '/editHelp'
  if 'nonModal' in hxPrefix :
    hxPrefix = hxPrefix.split('nonModal')[0].rstrip('/')
  if '?' in hxPrefix :
    hxPrefix = hxPrefix.split('?')[0]
  if '{' in hxPrefix :
    hxPrefix = hxPrefix.split('{')[0].rstrip('/')
  hxName = hxPrefix.replace('/', '_').lstrip('_')
  return (hxUrl, hxPrefix, hxName)

def checkRoutes() :
  print("  Checking routes")
  knownRoutes = set()
  for aRoute in routes :
    _, routePrefix, _ = sanitizeUrl(aRoute.path)
    knownRoutes.add(routePrefix)

  problemFound = False
  for aPagePartName, aPagePart in pageParts.items():
    # testName = aPagePartName.replace('.', '_')
    for someMetaData in aPagePart.metaData :
      hxGet = someMetaData['hxGet']
      if hxGet and hxGet.strip(')') not in ['None', 'hxGet'] :
        hxGet, hxGetPrefix, hxGetName = sanitizeUrl(hxGet)
        if hxGetPrefix not in knownRoutes :
          problemFound = True
          print(f"\nCheck PagePart: {aPagePartName}")
          print(" For the following errors:")
          print(f"   hxGet: {hxGetPrefix} {hxGetName} {hxGet}")
      hxPost = someMetaData['hxPost']
      if hxPost and hxPost.strip(')') not in ['None', 'hxPost'] :
        hxPost, hxPostPrefix, hxPostName = sanitizeUrl(hxPost)
        if hxPostPrefix not in knownRoutes :
          problemFound = True
          print(f"\nCheck PagePart: {aPagePartName}")
          print(" For the following errors:")
          print(f"  hxPost: {hxPostPrefix} {hxPostName} [{hxPost}]")
  return problemFound

sqlRegExpStrs = [
  r"IndexSql",
  r"SelectSql",
  r"InsertSql",
  r"UpdateSql",
  r"DeleteSql",
]
sqlRegExp = re.compile('|'.join(sqlRegExpStrs))

sqlTablesRexExp = re.compile(
  r"\.(sql|tables)\(([^\)]*)", re.MULTILINE
)

knownSqlPageParts = [

  # classes
  'app.people.classes.listClasses',
  'app.people.classes.postSaveNewClass',
  'app.people.classes.putUpdateAClass',

  # classes / borrowers / borrowersFTS
  'app.people.classes.deleteAnEmptyClass',
  'app.people.borrowers.postSaveNewBorrower',
  'app.people.borrowers.putUpdatedBorrower',
  'app.people.classesBorrowers.putUpdatePupilsInAClass',
  'app.people.classesBorrowers.listPupilsInAClassTable',
  'app.people.classesBorrowers.updatePupilsInClassForm',
  'app.people.borrowers.editBorrowerForm',

  # itemsInfo
  'app.books.itemsInfo.postSaveNewItemsInfo',
  'app.books.itemsInfo.putUpdateAnItemsInfo',
  'app.books.itemsInfo.getEditAnItemsInfoForm',

  # itemsInfo / itemsPhysical / itemsFTS
  'app.books.itemsPhysical.postSaveNewItemsPhysical',
  'app.books.itemsPhysical.putUpdateAnItemsPhysical',

  # borrowers / itemsInfo / itemsPhysical / itemsBorrowed
  'app.books.itemsPhysical.getEditItemsPhysicalForm',
  'app.books.itemsBorrowed.postSaveNewItemsBorrowed',
  'app.books.itemsBorrowed.putUpdateAnItemsBorrowed',
  'app.books.itemsBorrowed.getEditItemsBorrowedForm',
  'app.tasks.booksCheckedOut.booksCheckedOut',
  'app.utils.finders.getReturnABook'

]

knownSqlPageParts = set(knownSqlPageParts)

def findPagePartsUsingSql() :
  unknownSqlPageParts = {}
  for aPagePartName, aPagePart in pageParts.items() :
    matches = set()
    tables  = set()
    for aMatch in sqlRegExp.finditer(aPagePart.src) :
      matches.add(aMatch.group(0))
    if matches :
      for aTableMatch in sqlTablesRexExp.finditer(aPagePart.src) :
        someTables = ' '.join(aTableMatch.group(0).strip().split())
        if someTables.startswith('.sql') :
          someTables = someTables.removeprefix('.sql(').strip()
          someTables = someTables.split('{')[0].strip()
        elif someTables.startswith('.tables') :
          someTables = someTables.removeprefix('.tables(').strip()
        for aTable in someTables.split(',') :
          tables.add(aTable.strip())
      if aPagePartName not in knownSqlPageParts :
        matches = sorted(matches)
        unknownSqlPageParts[aPagePartName] = {
          'sql'    : ', '.join(matches),
          'tables' : ', '.join(tables)
        }
  if unknownSqlPageParts :
    print("\nSql using pageParts which have not been tested:")
    for aPagePartName, someMatches in unknownSqlPageParts.items() :
      print('  ' + aPagePartName)
      print('    ' + someMatches['sql'])
      print('      ' + someMatches['tables'])
    print("")
    return True
  return False

returnsRegExp = re.compile(r'return\s+[^\s\(]+[\s\(]')

methodsKnownToReturnCorrectly = [
  'schoolLib.app.people.borrowers.getShowBorrowerInfo',
  'schoolLib.app.people.borrowers.editBorrowerForm',
  'schoolLib.app.people.classes.listClasses',
  'schoolLib.app.books.itemsInfo.getShowItemsInfo',
  'schoolLib.app.books.itemsInfo.editItemsInfoForm',
  'schoolLib.app.books.itemsBorrowed.editItemsBorrowedForm',
]

knownPagePartReturns = [
  'app.admin.login.getLoginForm',  # (1)
  'app.admin.login.logoutPage',  # (1)
  'app.admin.login.postLoginPage',  # (1)
  'app.admin.menu.adminMenu',  # (1)
  'app.books.itemsBorrowed.getEditItemsBorrowedForm',  # (2)
  'app.books.itemsBorrowed.getNewItemsBorrowedForm',  # (2)
  'app.books.itemsBorrowed.postSaveNewItemsBorrowed',  # (1)
  'app.books.itemsBorrowed.putUpdateAnItemsBorrowed',  # (1)
  'app.books.itemsInfo.getEditAnItemsInfoForm',  # (2)
  'app.books.itemsInfo.getNewItemsInfoForm',  # (1)
  'app.books.itemsInfo.getShowItemsInfo',  # (1)
  'app.books.itemsInfo.postSaveNewItemsInfo',  # (1)
  'app.books.itemsInfo.putUpdateAnItemsInfo',  # (1)
  'app.books.itemsPhysical.getEditItemsPhysicalForm',  # (2)
  'app.books.itemsPhysical.getItemsPhysicalShow',  # (2) return theComponent | return MarkdownDiv(  # noqa
  'app.books.itemsPhysical.getNewItemsPhysicalForm',  # (2)
  'app.books.itemsPhysical.postSaveNewItemsPhysical',  # (2)
  'app.books.itemsPhysical.putUpdateAnItemsPhysical',   # (2)
  'app.books.menu.booksMenu',  # (1)
  'app.books.menu.getTakeOutABookForm',  # (1)
  'app.books.returnBooks.getReturnBooksPage',  # (1)
  'app.home.home.editHelpPage',  # (1) return HelpEditorModalDialog(
  'app.home.home.getHomeMenu',  # (1)
  'app.home.home.helpPages',  # (1) return getHelpPage(
  'app.home.home.homePage',  # (1)
  'app.home.home.postHelpPages',  # (1) return postHelpPage(
  'app.people.borrowers.getBorrowerReturnBook',  # (2)
  'app.people.borrowers.getEditABorrowerForm',  # (1)
  'app.people.borrowers.getNewBorrowerForm',  # (1)
  'app.people.borrowers.getShowBorrowerInfo',  # (3)
  'app.people.borrowers.postSaveNewBorrower',  # (1)
  'app.people.borrowers.putUpdatedBorrower',  # (1)
  'app.people.classes.addAClass',  # (1)
  'app.people.classes.deleteAnEmptyClass',  # (1)
  'app.people.classes.getEditAClassForm',  # (2)
  'app.people.classes.listClasses',  # (1)
  'app.people.classes.postSaveNewClass',  # (1)
  'app.people.classes.putUpdateAClass',  # (1)
  'app.people.classesBorrowers.getUpdatePupilsInAClassForm',  # (1)
  'app.people.classesBorrowers.listPupilsInAClassTable',  # (1)
  'app.people.classesBorrowers.putUpdatePupilsInAClass',  # (1)
  'app.people.menu.peopleMenu',  # (1)
  'app.tasks.booksCheckedOut.booksCheckedOut',  # (1)
  'app.tasks.menu.tasksMenu',   # (1)
  'app.utils.finders.getFindAnItemForm',  # (1)
  'app.utils.finders.getFindBorrowerForm',  # (1)
  'app.utils.finders.getReturnABook',  # (2) return OobCollection( | return Text(  # noqa
  'app.utils.finders.getTakeOutABook',  # (2) return Div(
  'app.utils.finders.postReturnBooksSearch',  # (1) return schoolLib.app.utils.finders.searchForThings( # noqa
  'app.utils.finders.postSearchForAnItem',  # (1) return schoolLib.app.utils.finders.searchForThings( # noqa
  'app.utils.finders.postSearchForBorrower',  # (1) return schoolLib.app.utils.finders.searchForThings(  # noqa
  'app.utils.finders.postTakeOutABookSearch',  # (2) return Div( | return schoolLib.app.utils.finders.searchForThings(  # noqa
  'app.utils.metaStructure.listPageParts',  # (1)
  'app.utils.metaStructure.listRoutes',  # (1)
  'app.utils.metaStructure.provideUIOverview',  # (1)
]

# knownPagePartReturns = set(knownPagePartReturns)
knownPagePartReturns = set()

def collectRouteMethods() :
  routeMethods = set()
  for aRoute in routes :
    anEndpoint = f'{aRoute.endpoint.__module__.removeprefix('schoolLib.')}.{aRoute.endpoint.__name__}'  # noqa
    routeMethods.add(anEndpoint)
  return sorted(routeMethods)

def collectUnknownPageParts(routeMethods) :
  unknownPagePartReturns = {}
  for aRouteMethod in routeMethods :
    if aRouteMethod not in pageParts : continue
    aPagePart = pageParts[aRouteMethod]
    matches = []
    for aMatch in returnsRegExp.finditer(aPagePart.src) :
      theMatch = aMatch.group(0).strip()
      matches.append(theMatch)
    if matches :
      if aRouteMethod not in knownPagePartReturns :
        unknownPagePartReturns[aRouteMethod] = matches
  return unknownPagePartReturns

def checkPagePartReturns() :
  routeMethods = collectRouteMethods()
  unknownPagePartReturns = collectUnknownPageParts(routeMethods)
  if unknownPagePartReturns :
    print("\npagePart return which have not been considered:")
    for aPagePartName, someMatches in unknownPagePartReturns.items() :
      print(f"  '{aPagePartName}',  # ({len(someMatches)})")
      for aMatch in someMatches :
        if 'RefreshMainContent' in aMatch    : continue
        if 'HtmlPage' in aMatch              : continue
        if 'goToHomePage' in aMatch          : continue
        if 'Menu' in aMatch and aPagePartName.endswith('Menu') :
          continue
        returnMethod = aMatch.split(' ')
        if 1 < len(returnMethod) :
          returnMethod = returnMethod[1].strip('(')
          if returnMethod in methodsKnownToReturnCorrectly :
            continue
        if aMatch == 'return your'           : continue
        print('    ' + aMatch)
    print("")
    return True
  return False

def loadSchema() :
  schema = {}
  with open(os.path.join('schoolLib', 'setup', 'schema.yaml')) as sFile :
    schema = yaml.safe_load(sFile.read())
  classes = {}
  for aKey, aValue in schema.items() :
    aClass, aField = aKey.split('.')
    if aClass not in classes :
      classes[aClass] = {}
    classes[aClass][aField] = aValue
  return classes

def checkSchema() :
  problemFound = False
  # schema = loadSchema()
  # print(yaml.dump(schema))
  # print(yaml.dump(sorted(pageParts.keys())))
  return problemFound

def runSanityChecks() :
  print("Running sanity tests...")

  setupApp()
  computePagePartUsers()
  problemFound = False
  problemFound |= findPagePartsUsingSql()
  problemFound |= checkPagePartReturns()
  problemFound |= checkRoutes()
  problemFound |= checkSchema()

  if problemFound :
    print("Please fix the above problems")
    sys.exit(1)

  print("  ... The sanity checks found no problems")

