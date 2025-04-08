
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

knownSqlPageParts = [
  #  'app.books.itemsInfo.putUpdateAnItemsInfo'
]
knownSqlPageParts = set(knownSqlPageParts)

def findPagePartsUsingSql() :
  unknownSqlPageParts = {}
  for aPagePartName, aPagePart in pageParts.items() :
    matches = set()
    for aMatch in sqlRegExp.finditer(aPagePart.src) :
      matches.add(aMatch.group(0))
    if matches :
      if aPagePartName not in knownSqlPageParts :
        matches = sorted(matches)
        unknownSqlPageParts[aPagePartName] = ', '.join(matches)
  if unknownSqlPageParts :
    print("\nSql using pageParts which have not been tested:")
    for aPagePartName, someMatches in unknownSqlPageParts.items() :
      print('  ' + aPagePartName)
      print('    ' + someMatches)
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
  # problemFound |= checkRoutes()
  # problemFound |= checkSchema()

  if problemFound :
    print("Please fix the above problems")
    sys.exit(1)

  print("  ... The sanity checks found no problems")

