"""
A simple tool to access the database
"""

# # TODO need to protect from `'` used by user.

# from contextlib import contextmanager
from datetime import date, timedelta
import os
# import sqlite3
# import traceback
import yaml

from schoolLib.setup.configuration import config

###############################################################
# We maintain a simple schema facitlity to ensure we know what
# type of field we are manipulating
#
# The schema is stored in an external YAML file and consists
# of a simple list of fields and types. Fields are all named
#   <tableName>.<fieldName>

schemaFields = {}
schemaTables = {}

def loadSchema() :
  schemaPath = os.path.join(
    os.path.dirname(__file__),
    'schema.yaml'
  )
  schemaDict = {}
  with open(schemaPath) as schemaFile :
    schemaDict = yaml.safe_load(schemaFile.read())
  for aTableField, aType in schemaDict.items() :
    aTable, aField = aTableField.split('.')
    if aTable not in schemaTables :
      schemaTables[aTable] = {}
    schemaTables[aTable][aField] = aType
    schemaFields[aTableField]    = aType
    schemaFields[aField]         = aType
  # print(yaml.dump(schemaFields))
loadSchema()

###############################################################
# We provide a very simple SQL statement builder...
#
# The allows us to know enough about the structure of the SQL
# to be able make a list of dicts from the results

def sqliteEscapeSingleQuotes(aStr) :
  return aStr.replace(r"'", r"''")

def sqliteUnEscapeSingleQuotes(aStr) :
  return aStr.replace(r"''", r"'")

class SqlBuilder :

  def __init__(self) :
    self.whereList    = []
    self.orderByList  = []
    self.orderAsc     = True
    self.limitToValue = None
    self.groupByList  = []

  def whereField(self, fieldA, fieldB, operator='=') :
    self.whereList.append(f"{fieldA} {operator} {fieldB}")
    return self

  def whereValue(self, field, value, operator='=') :
    wrappedValue = str(value)
    if field in schemaFields and schemaFields[field] == "text" :
      wrappedValue = f"'{sqliteEscapeSingleQuotes(value)}'"
    self.whereList.append(f"{field} {operator} {wrappedValue}")
    return self

  def _buildWhere(self) :
    subCmd = ""
    if self.whereList :
      subCmd += " WHERE "
      subCmd += " AND ".join(self.whereList)
    return subCmd

  def orderAscBy(self, *keys) :
    self.orderByList.extend(keys)
    self.orderAsc = True
    return self

  def orderDescBy(self, *keys) :
    self.orderByList.extend(keys)
    self.orderAsc = False
    return self

  def _buildOrderBy(self) :
    subCmd = ""
    if self.orderByList :
      subCmd += " ORDER BY "
      subCmd += ", ".join(self.orderByList)
      if not self.orderAsc :
        subCmd += " DESC "
    return subCmd

  def limitTo(self, anExp) :
    self.limitToValue = anExp
    return self

  def _buildLimitTo(self) :
    subCmd = ""
    if self.limitToValue :
      subCmd = f" LIMIT {self.limitToValue}"
    return subCmd

  def groupBy(self, *keys) :
    self.groupByList.extend(keys)
    return self

  def _buildGroupBy(self) :
    subCmd = ""
    if self.groupByList :
      subCmd += " GROUP BY "
      subCmd += ', '.join(self.groupByList)
    return subCmd

class IndexSql(SqlBuilder) :

  def sql(self, indexName, tableName, *fields) :
    return ""

# class FullTextSearchIndexSql(SqlBuilder) :
#
#   def sql(self, indexName, tableName, *fields) :
#     # see: https://sqlite.org/fts5.html
#     return ""

class SelectSql(SqlBuilder) :

  def __init__(self) :
    super().__init__()
    self.fieldsList  = []
    self.tablesList  = []
    self.joinsList   = []

  def fields(self, *fields) :
    self.fieldsList.extend(fields)
    return self

  def tables(self, *tables) :
    self.tablesList.extend(tables)
    return self

  def join(self, aTable, fieldA, fieldB, joinType="", operator="=") :
    self.joinsList.append(
      f" {joinType} JOIN {aTable} ON {fieldA} {operator} {fieldB}"
    )
    return self

  def sql(self) :
    cmd = "SELECT DISTINCT "
    cmd += ", ".join(self.fieldsList)
    cmd += " FROM "
    cmd += ", ".join(self.tablesList)
    cmd += " ".join(self.joinsList)
    cmd += self._buildWhere()
    cmd += self._buildGroupBy()
    cmd += self._buildOrderBy()
    cmd += self._buildLimitTo()
    return cmd

  def parseResults(self, results, fetchAll=True) :
    fixedFields = []
    for aField in self.fieldsList :
      newField = aField
      if '.' in aField :
        newField = aField.replace('.', '_')
      fixedFields.append(newField)
    newResults = []
    if results :
      for aRow in results :
        newRow = {}
        for aFieldNum in range(len(self.fieldsList)) :
          newRow[fixedFields[aFieldNum]] = aRow[aFieldNum]
        newResults.append(newRow)
        if not fetchAll :
          break
    return newResults

class InsertSql(SqlBuilder) :

  def sql(self, table, values) :

    keysList = []
    valuesList = []
    for aKey, aValue in values.items() :
      if aKey == 'id' :
        continue
      keysList.append(aKey)
      escapedValue = str(aValue)
      if aKey in schemaFields and schemaFields[aKey] == "text" :
        escapedValue = f"{sqliteEscapeSingleQuotes(aValue)}"
      valuesList.append(escapedValue)

    cmd = "INSERT INTO "
    cmd += table
    cmd += " ( "
    cmd += ", ".join(keysList)
    cmd += " ) VALUES ( "
    cmd += ", ".join(['?'] * len(valuesList))
    cmd += ")"
    # print(f"InsertSql cmd: [{cmd}]")
    values = tuple(valuesList)
    # print(f"InsertSql values: [{values}]")

    return (cmd, values)

class UpdateSql(SqlBuilder) :

  def sql(self, table, values) :

    setList = []
    for aKey, aValue in values.items() :
      if aKey == 'id' :
        continue
      setList.append(f"{aKey} = '{sqliteEscapeSingleQuotes(aValue)}'")

    cmd = "UPDATE "
    cmd += table
    cmd += " SET "
    cmd += ", ".join(setList)
    cmd += self._buildWhere()
    return cmd

class DeleteSql(SqlBuilder) :

  def sql(self, table) :

    if not self.whereList :
      print("CAN NOT DELETE WITHOUT A WHERE sub command")
      return

    cmd = "DELETE FROM "
    cmd += table
    cmd += self._buildWhere()
    return cmd

###############################################################
# Some simple database handling utilities
#
# deal with classes

def getClasses(db, selectedClass=None) :
  selectSql = SelectSql(
  ).fields("id", "name", "classOrder", "desc", "colour"
  ).tables("classes"
  ).orderAscBy('classOrder'
  )
  print(selectSql.sql())
  results = selectSql.parseResults(db.execute(selectSql.sql()))
  theClasses = {}
  for aClass in results :
    aClass['selected']   = ''
    theClasses[aClass['id']] = aClass

  if selectedClass :
    selectedClass = int(selectedClass)
    if selectedClass in theClasses :
      theClasses[selectedClass]['selected'] = 'selected'

  return theClasses

def getSortedClasses(theClasses) :
  sortOrder = sorted(
    theClasses.keys(),
    key=lambda aClassId : theClasses[aClassId]['classOrder']
  )
  sortedClasses = []
  for aClassId in sortOrder :
    sortedClasses.append(theClasses[aClassId])
  return sortedClasses

def getOrderedClassList(db, selectedClass=None) :
  classes = getClasses(db, selectedClass=selectedClass)
  return getSortedClasses(classes)

###############################################################
# Some simple database handling utilities
#
# deal with help pages

def getHelpPageHtml(db, aHelpPage) :
  selectSql = SelectSql(
  ).fields("content"
  ).tables("helpPages"
  ).whereValue('path', aHelpPage)
  print(selectSql.sql())
  results = selectSql.parseResults(
    db.execute(selectSql.sql()),
    fetchAll=False
  )
  if results :
    print(yaml.dump(sqliteUnEscapeSingleQuotes(results[0]['content'])))
    return sqliteUnEscapeSingleQuotes(results[0]['content'])
  return None

# book handling

def findPhysicalBookInItemsBorrowed(db, itemsPhysicalId) :
  selectSql = SelectSql(
  ).fields('id', 'borrowersId', 'itemsPhysicalId',
  ).tables('itemsBorrowed'
  ).whereValue(
    'itemsPhysicalId', itemsPhysicalId
  )
  print(selectSql.sql())
  results = selectSql.parseResults(
    db.execute(selectSql.sql()),
    fetchAll=False
  )
  if results :
    return results[0]
  return None

def dbReturnABook(db, itemsBorrowedId) :
  # find the book in the itemsBorrowed table (to ensure it IS there)
  selectSql = SelectSql(
  ).fields(
    'itemsBorrowed.id', 'borrowersId', 'itemsPhysicalId', 'dateBorrowed'
  ).tables('itemsBorrowed'
  ).whereValue(
    'itemsBorrowed.id', itemsBorrowedId
  )
  itemBorrowedRow = selectSql.parseResults(
    db.execute(selectSql.sql()),
    fetchAll=False
  )
  if not itemBorrowedRow :
    return False
  itemBorrowedRow = itemBorrowedRow[0]

  print("Returned:")
  print(yaml.dump(itemBorrowedRow))

  # delete the book from the itemsBorrowed table
  db.execute(
    DeleteSql().whereValue('id', itemsBorrowedId).sql('itemsBorrowed')
  )

  # insert the book into the itemsReturned table
  db.execute(*InsertSql().sql('itemsReturned', {
    'borrowersId'     : itemBorrowedRow['borrowersId'],
    'itemsPhysicalId' : itemBorrowedRow['itemsPhysicalId'],
    'dateBorrowed'    : itemBorrowedRow['dateBorrowed'],
    'dateReturned'    : date.today()
  }))

  # commit these changes
  db.commit()
  return True

def dbTakeOutABook(db, borrowerId, itemsPhysicalId) :
  # find the book in the itemsBorrowed table (to ensure it IS NOT there)
  itemBorrowedRow = findPhysicalBookInItemsBorrowed(db, itemsPhysicalId)
  if itemBorrowedRow :
    return False

  # insert the book into the itemsBorrowed table
  today = date.today()
  loanPeriod = 7
  if 'loanPeriod' in config :
    loanPeriod = config['loanPeriod']
  db.execute(*InsertSql().sql('itemsBorrowed', {
    'borrowersId'     : borrowerId,
    'itemsPhysicalId' : itemsPhysicalId,
    'dateBorrowed'    : today,
    'dateDue'         : today + timedelta(days=loanPeriod)
  }))

  # commit these changes
  db.commit()
  return True
