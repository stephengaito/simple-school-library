"""
A simple tool to access the database
"""

## TODO need to protect from `'` used by user.

from contextlib import contextmanager
import os
import sqlite3
import yaml

from schoolLib.setup.exceptions    import SLException
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

loadSchema()

###############################################################
# We provide a very simple SQL statement builder...
#
# The allows us to know enough about the structure of the SQL
# to be able make a list of dicts from the results

class SqlBuilder :

  def __init__(self) :
    self.whereList   = []
    self.orderByList = []

  def whereField(self, fieldA, fieldB, operator='=') :
    self.whereList.append(f"{fieldA} {operator} {fieldB}")
    return self

  def whereValue(self, field, value, operator='=') :
    wrappedValue = str(value)
    if field in schemaFields and schemaFields[field] != "INTEGER" :
      wrappedValue = f"'{value}'"
    self.whereList.append(f"{field} {operator} {value}")
    return self

  def _buildWhere(self) :
    subCmd = ""
    if self.whereList :
      subCmd += " WHERE "
      subCmd += " AND ".join(self.whereList)
    return subCmd

  def orderBy(self, *keys) :
    self.orderByList.extend(keys)
    return self

  def _buildOrderBy(self) :
    subCmd = ""
    if self.orderByList :
      subCmd += " ORDER BY "
      subCmd += ", ".join(self.orderByList)
    return subCmd

class CreateSql(SqlBuilder) :

  def sql(self, table) :
    if table not in schemaTables :
      print("CAN NOT CREATE a table if it is not in the schema.yaml")
      return

    fieldList = []
    for aField, aType in schemaTables[table].items() :
      aFieldStmt = f"{aField} {aType.upper()}"
      if aField == "id" :
        aFieldStmt += " PRIMARY KEY AUTOINCREMENT"
      fieldList.append(aFieldStmt)

    cmd = "CREATE TABLE IF NOT EXISTS "
    cmd += table
    cmd += " ( "
    cmd += ", ".join(fieldList)
    cmd += " ) "
    return cmd

class IndexSql(SqlBuilder) :

  def sql(self, indexName, tableName, *fields) :
    return ""

class FullTextSearchIndexSql(SqlBuilder) :

  def sql(self, indexName, tableName, *fields) :
    # see: https://sqlite.org/fts5.html
    return ""

class SelectSql(SqlBuilder) :

  def __init__(self) :
    super().__init__()
    self.fieldsList  = []
    self.tablesList  = []

  def fields(self, *fields) :
    self.fieldsList.extend(fields)
    return self

  def tables(self, *tables) :
    self.tablesList.extend(tables)
    return self

  def sql(self) :
    cmd = "SELECT "
    cmd += ", ".join(self.fieldsList)
    cmd += " FROM "
    cmd += ", ".join(self.tablesList)
    cmd += self._buildWhere()
    cmd += self._buildOrderBy()
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
        if not fetchAll : break
    return newResults

class InsertSql(SqlBuilder) :

  def sql(self, table, values) :

    keysList = []
    valuesList = []
    for aKey, aValue in values.items() :
      if aKey == 'id' : continue
      keysList.append(aKey)
      valuesList.append(f"'{aValue}'")

    cmd = "INSERT INTO "
    cmd += table
    cmd += " ( "
    cmd += ", ".join(keysList)
    cmd += " ) VALUES ( "
    cmd += ", ".join(valuesList)
    cmd += ")"
    return cmd

class UpdateSql(SqlBuilder) :

  def sql(self, table, values) :

    setList = []
    for aKey, aValue in values.items() :
      if aKey == 'id' : continue
      setList.append(f"{aKey} = '{aValue}'")

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
  ).orderBy('classOrder'
  )

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
# A simple database context manager
#
# This allows us to connect to the database once per page load
# but we can perform multiple selects and/or updates per page

@contextmanager
def getDatabase(path=None, asCursor=False) :
  if not path :
    path = ":memory:"
    if 'database' in config :
      path = config['database']
  try :
    db = sqlite3.connect(path)
    try :
      if asCursor :  yield db.cursor()
      else        :  yield db
    finally :
      db.close()
  except Exception as err :
    print(f"Could not connect to the database: [{path}]")
    print(repr(err))
    raise SLException(
      f"Could not open database [{path}]",
      'Trying to open the database',
      'Have you configured the database properly?',
      repr(err)
    )

#def selectUsing(anSQLselection) :
#  with getDatabase(asCursor=True) as cursor:
#    cursor.execute(anSQLselection)
#    return cursor.fetchall()