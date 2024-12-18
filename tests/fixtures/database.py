
import copy
import pytest
import sqlite3

from schoolLib.tools.dbUpdates.utils import knownDbVersions
from schoolLib.tools.updateDatabase  import updateDatabase

# create an in-memory SQLite3 database and populate it with the initial
# tables and indexes

@pytest.fixture
def database(scope="module", autouse=True) :
  db = sqlite3.connect(":memory:")
  updateDatabase(db, copy.deepcopy(knownDbVersions), verbose=False)
  return db

