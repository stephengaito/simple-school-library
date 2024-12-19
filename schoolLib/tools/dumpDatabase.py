
import sqlite3

from schoolLib.setup import config, loadedConfig
from schoolLib.tools.sslIterdump import ssl_iterdump

loadedConfig('config.yaml')

def cli() :
  try :
    dbPath = config['database']
    db = sqlite3.connect(dbPath)
    for line in ssl_iterdump(db) :
      print(line)
  except Exception as err :
    print(repr(err))

