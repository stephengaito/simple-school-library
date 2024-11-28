
import sys
import yaml

from schoolLib.setup import loadedConfig, config

def databasePathUsage(progName) :
  print(f"""
usage: {progName} <-c <configPath> |-d <databasePath> >

where:
  <-c|-d> is one or other of the two options `-c` or `-d` below

options:
  -c  --config    A path to a configuration file
  -d  --db        A path to a SQLite3 database
  -h, --help      Print this message
""")
  sys.exit(1)

def getDatabasePath(progName) :
  if len(sys.argv) < 3 :
    databasePathUsage(progName)

  theOption   = sys.argv[1]
  theArgument = sys.argv[2]

  dbPath = None
  if '-h' in theOption :
    databasePathUsage(progName)
  elif '-c' in theOption :
    loadedConfig(theArgument, reportErrors=True)
    if 'database' not in config :
      print(yaml.dump(config))
      print("No database specified in config file")
      sys.exit(1)
    dbPath = config['database']
  elif '-d' in theOption :
    dbPath = theArgument

  if not dbPath :
    print("One or other of the '-c' or '-d' options MUST be provided")
    sys.exit(1)

  print(f"Working with the {dbPath} SQLite database")
  return dbPath

