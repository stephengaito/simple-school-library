
import base64
from getpass import getpass
import hashlib
import os
import sqlite3
import sys

from starlette_login.mixins import UserMixin

from schoolLib.setup.configuration import config, loadedConfig

# see: https://starlette-login.readthedocs.io/en/stable/

class SLibUser(UserMixin) :
  @property
  def is_authenticated(self) :
    return True

  @property
  def display_name(self) :
    return 'admin user (slib)'

  @property
  def identity(self) :
    return 'slib'

class OtherUser(UserMixin) :
  @property
  def is_authenticated(self) :
    return False

  @property
  def display_name(self) :
    return 'general user'

  @property
  def identity(self) :
    return 'other'

def loadUsers(request, userId) :
  theUser = OtherUser()
  if userId == 'slib' : theUser = SLibUser()
  print(f"Loaded user: {theUser.display_name}")
  return theUser

# see: https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/     # noqa
# See: https://www.askpython.com/python/examples/storing-retrieving-passwords-securely   # noqa

def encryptSlibPassword(plainTextPassword, salt) :
  hashValue = hashlib.pbkdf2_hmac(
    'sha256',                           # hashing algorithm
    plainTextPassword.encode('utf-8'),  # in bytes
    salt,                               # in bytes
    100000                              # iterations
  )
  return base64.b64encode(salt + hashValue).decode('utf-8')

def authenticateSlibUser(password, db) :
  try :
    results = db.execute("SELECT * FROM accounts WHERE username = 'slib'")
    slib, hashedPassword, salt = results.fetchone()
    salt = base64.b64decode(salt)
    encryptedPassword = encryptSlibPassword(password, salt)
    if hashedPassword == encryptedPassword : return True
  except Exception as err :
    print(repr(err))
  return False

def passwordCliUsage() :
  print("""
usage: sPasswordHello [new|help]

  With no arguments slPassword will check the user 'slib's password.

  With an argument of 'new' slPassword will assign the user 'slib'
    the given password.

  With any other argument (or 'help') slPassword will print this help.
""")
  sys.exit(1)

def passwordCli() :

  # load the School Library configuration (to get location of database)
  loadedConfig('config.yaml')
  dbPath = config['database']
  db = sqlite3.connect(dbPath)

  createNewPassword     = False
  if 1 < len(sys.argv) :
    if sys.argv[1].startswith('new') : createNewPassword = True
    else : passwordCliUsage()

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
