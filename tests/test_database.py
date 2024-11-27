
import sqlite3
import yaml

# import pytest

from schoolLib.setup.database import schemaTables, schemaFields, SelectSql, \
  InsertSql, UpdateSql, DeleteSql, CreateSql, getClasses, getSortedClasses

# from utils import getResponseBody

def test_loadSchema() :
  assert 'borrowers'     in schemaTables
  assert 'classes'       in schemaTables
  assert 'itemsBorrowed' in schemaTables
  assert 'itemsInfo'     in schemaTables
  assert 'itemsPhysical' in schemaTables

  assert 'id' in schemaTables['borrowers']
  assert 'id' in schemaTables['classes']
  assert 'id' in schemaTables['itemsBorrowed']
  assert 'id' in schemaTables['itemsInfo']
  assert 'id' in schemaTables['itemsPhysical']

  assert schemaTables['borrowers']['id']     == 'integer'
  assert schemaTables['classes']['id']       == 'integer'
  assert schemaTables['itemsBorrowed']['id'] == 'integer'
  assert schemaTables['itemsInfo']['id']     == 'integer'
  assert schemaTables['itemsPhysical']['id'] == 'integer'

  assert schemaFields['borrowers.id']     == 'integer'
  assert schemaFields['classes.id']       == 'integer'
  assert schemaFields['itemsBorrowed.id'] == 'integer'
  assert schemaFields['itemsInfo.id']     == 'integer'
  assert schemaFields['itemsPhysical.id'] == 'integer'

def test_select() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE' not in cmd

def test_selectWhere() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).whereValue('id', 2
  ).whereValue('firstName', 'stephen'
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE'     in cmd
  assert '='         in cmd
  assert 'stephen'   in cmd
  assert "id = 2"    in cmd

def test_selectOrderAscBy() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).orderAscBy('familyName'
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE' not in cmd
  assert 'ORDER BY familyName' in cmd
  assert 'DESC'  not in cmd

def test_selectOrderDescBy() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).orderDescBy('familyName'
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE' not in cmd
  assert 'ORDER BY familyName' in cmd
  assert 'DESC'      in cmd

def test_selectWhereOrderAscBy() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).whereValue('id', 2
  ).whereValue('firstName', 'stephen'
  ).orderAscBy('familyName'
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE'     in cmd
  assert '='         in cmd
  assert 'stephen'   in cmd
  assert "id = 2"    in cmd
  assert 'ORDER BY familyName' in cmd
  assert 'DESC'  not in cmd

def test_selectWhereOrderDescBy() :
  cmd = SelectSql().fields(
    "id", "firstName", "familyName"
  ).tables(
    "borrowers"
  ).whereValue('id', 2
  ).whereValue('firstName', 'stephen'
  ).orderDescBy('familyName'
  ).sql()
  print(cmd)
  assert 'SELECT' in cmd
  assert 'firstName' in cmd
  assert 'borrowers' in cmd
  assert 'WHERE'     in cmd
  assert '='         in cmd
  assert 'stephen'   in cmd
  assert "id = 2"    in cmd
  assert 'ORDER BY familyName' in cmd
  assert 'DESC'      in cmd

def test_parseResults() :
  results = SelectSql().fields(
    "id", "firstName", "familyName"
  ).parseResults([
    [1, 'Stephen', 'Gaito'],
    [2, 'Maureen', 'Greyson']
  ])
  # print(yaml.dump(results))
  firstResult = results[0]
  assert 'familyName' in firstResult
  assert firstResult['familyName'] == 'Gaito'
  secondResult = results[1]
  assert 'firstName' in secondResult
  assert secondResult['firstName'] == 'Maureen'

def test_insert() :
  cmd = InsertSql().sql("borrowers", {
    "id" : 1,
    "firstName" : 'Stephen',
    "familyName" : 'Gaito'
  })
  print(cmd)
  assert 'INSERT INTO' in cmd[0]
  assert 'borrowers'   in cmd[0]
  assert 'firstName'   in cmd[0]
  assert 'WHERE'   not in cmd[0]
  assert 'VALUES'      in cmd[0]
  assert 'Stephen'     in cmd[1]
  assert 'Gaito'       in cmd[1]

def test_update() :
  cmd = UpdateSql(
  ).whereValue('familyName', 'Gaito'
  ).sql("borrowers", {
    "firstName" : 'Steve'
  })
  print(cmd)
  assert 'UPDATE'     in cmd
  assert 'borrowers'  in cmd
  assert 'SET'        in cmd
  assert 'firstName'  in cmd
  assert '='          in cmd
  assert 'Steve'      in cmd
  assert 'WHERE'      in cmd
  assert 'familyName' in cmd
  assert 'Gaito'      in cmd

def test_delete() :
  cmd = DeleteSql(
  ).whereValue('familyName', 'Gaito'
  ).sql("borrowers")
  print(cmd)
  assert 'DELETE'     in cmd
  assert 'borrowers'  in cmd
  assert 'WHERE'      in cmd
  assert 'familyName' in cmd
  assert '='          in cmd
  assert 'Gaito'      in cmd

def test_create() :
  cmd = CreateSql().sql("borrowers")
  print(yaml.dump(schemaTables['borrowers']))
  print(cmd)
  assert 'CREATE TABLE IF NOT EXISTS'        in cmd
  assert 'borrowers'                         in cmd
  assert 'id'                                in cmd
  assert 'familyName'                        in cmd
  assert 'INTEGER PRIMARY KEY AUTOINCREMENT' in cmd
  assert 'TEXT'                              in cmd


def test_getDatabase() :
  results = []
  # we set the path explicitly so we do not use a local database.
  with sqlite3.connect(':memory:') as db :
    db.execute(CreateSql().sql("borrowers"))
    db.execute(*InsertSql().sql('borrowers', {
      "firstName" : 'Stephen',
      "familyName" : 'Gaito'
    }))
    db.commit()
    selectSql = SelectSql(
    ).fields("firstName", "familyName"
    ).tables('borrowers')
    results = selectSql.parseResults(
      db.execute(selectSql.sql())
    )
  print(yaml.dump(results))
  assert len(results) == 1
  assert isinstance(results[0], dict)
  assert 'firstName'  in results[0]
  assert 'familyName' in results[0]
  assert results[0]['firstName']  == 'Stephen'
  assert results[0]['familyName'] == 'Gaito'

def test_classes() :
  theClasses = {}
  sortedClasses = []
  # we set the path explicitly so we do not use a local database.
  with sqlite3.connect(':memory:') as db :
    db.execute(CreateSql().sql('classes'))
    db.execute(*InsertSql().sql('classes', {
      'name' : 'Oak class',
      'classOrder' : 10,
      'desc' : '',
      'colour' : '#000000'
    }))
    db.execute(*InsertSql().sql('classes', {
      'name' : 'Wise class',
      'classOrder' : 1,
      'desc' : '',
      'colour' : '#000000'
    }))
    db.commit()
    theClasses = getClasses(db, selectedClass=2)
    sortedClasses = getSortedClasses(theClasses)
  print(yaml.dump(theClasses))
  print(yaml.dump(sortedClasses))

  assert isinstance(theClasses, dict)
  assert isinstance(sortedClasses, list)

  assert 0 not in theClasses
  assert 1     in theClasses
  assert 2     in theClasses
  assert 3 not in theClasses
  assert len(theClasses) == 2

  assert 'classOrder' in theClasses[2]
  assert 'name'       in theClasses[2]
  assert 'desc'       in theClasses[2]
  assert 'colour'     in theClasses[2]
  assert 'selected'   in theClasses[2]
  assert theClasses[2]['selected'] == 'selected'
  assert theClasses[2]['name']     == 'Wise class'

  assert 'selected'   in theClasses[1]
  assert theClasses[1]['selected'] == ''

  assert len(sortedClasses) == 2
  assert sortedClasses[0]['classOrder'] == theClasses[2]['classOrder']
  assert sortedClasses[1]['classOrder'] == theClasses[1]['classOrder']
  assert sortedClasses[0]['name']       == theClasses[2]['name']
  assert sortedClasses[1]['name']       == theClasses[1]['name']

