
import inspect
import sqlite3
import yaml

from schoolLib.setup import *
from schoolLib.tools.sslIterdump import *

loadedConfig('config.yaml')

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)

    # get the helpPages schema
    cur = db.execute("""
    SELECT name, type, sql
    FROM sqlite_master
    WHERE sql NOT NULL
    AND type == 'table'
    AND name == 'helpPages'
    """)
    helpPagesCreateStmt = list(cur.fetchall())[0][2]

    # get the existing help pages
    cur = db.execute("SELECT path, content FROM helpPages")
    helpPages = list(cur.fetchall())

    # drop and recreate the helpPages table
    db.execute("DROP TABLE helpPages")
    db.commit()
    db.execute(helpPagesCreateStmt)
    db.commit()

    for aHelpPage in helpPages :
      db.execute("""
      INSERT INTO helpPages (path, content)
      VALUES(?,?)
      """, aHelpPage)
      db.commit()

    for line in ssl_iterdump(db, ['helpPages']) :
      print(line)
  except Exception as err :
    print(repr(err))

