
import base64
from getpass import getpass
import hashlib
import os
import sqlite3
import sys

from schoolLib.setup.configuration import config, loadedConfig

# see: https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
# See: https://www.askpython.com/python/examples/storing-retrieving-passwords-securely

def encryptSlibPassword(plainTextPassword, salt) :
  hashValue = hashlib.pbkdf2_hmac(
    'sha256', # hashing algorithm
    plainTextPassword.encode('utf-8'), # in bytes
    salt, #in bytes
    100000 # iterations
  )
  return base64.b64encode(salt + hashValue).decode('utf-8')

def authenticateSlibUser(password, db) :
  try :
    results = db.execute("SELECT * FROM accounts WHERE username = 'slib'")
    slib, hashedPassword, salt = results.fetchone()
    salt = base64.b64decode(salt)
    encryptedPassword = encryptSlibPassword(password, salt)
    if hashedPassword == encryptedPassword : return True
  except :
    pass
  return False

def cli() :

  # load the School Library configuration (to get location of database)
  loadedConfig('config.yaml')
  dbPath = config['database']
  db = sqlite3.connect(dbPath)

  createNewPassword     = False
  if 1 < len(sys.argv) :
    if sys.argv[1].startswith('new') : createNewPassword = True

  if createNewPassword :
    # Ask the user for the password
    passwordOK = False
    while not passwordOK :
      passwordA = getpass(" slib's NEW password: ")
      passwordB = getpass("NEW password (again): ")
      if passwordA != passwordB :
        print("\nPasswords do no match.... please try again\n")
      else :
        passwordOK = True

    # hash the password
    salt = os.urandom(16)
    hashedPassword = encryptSlibPassword(passwordA, salt)

    # store the password in the database
    db.execute("DROP TABLE IF EXISTS accounts")
    db.execute("""
      CREATE TABLE IF NOT EXISTS accounts (
        username  TEXT,
        password  TEXT,
        salt      TEXT
      )
    """)
    db.execute("""
      INSERT INTO accounts (username, password, salt)
      VALUES (?, ?, ?)
    """, ('slib', hashedPassword, base64.b64encode(salt) )
    )
    db.commit()

  else :  # check the existing password

    testPassword = getpass("check slib's password: ")
    if authenticateSlibUser(testPassword, db) :
      print("Authenticated slib !!!")
    else :
      print("Could not authenticate slib ;-( ")
