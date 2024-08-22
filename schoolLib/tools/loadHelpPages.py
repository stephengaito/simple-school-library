
import inspect
import sqlite3

from schoolLib.setup import *
from schoolLib.tools.sslIterdump import *

loadedConfig('config.yaml')

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)
    with open("tmp/helpPages.sql") as sqlFile :
      aStm = []
      for line in sqlFile :
        line = line.strip()
        aStm.append(line)
        if ';' in line :
          print(" ".join(aStm))
          aStm = []
  except Exception as err :
    print(repr(err))

