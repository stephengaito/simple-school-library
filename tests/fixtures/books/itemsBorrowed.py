
import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known items info to the database

romanBritainCopy1 = """
authenticated: True
theForm:
  dateBorrowed: 2025-04-11
  dateDue: 2025-04-18
"""

farmAnimalsCopy1 = """
authenticated: True
theForm:
  dateBorrowed: 2025-04-11
  dateDue: 2025-04-18
"""

# farmAnimalsCopy2 is NOT checked out

@pytest.fixture
def addSomeItemsBorrowed(database) :

  pageData = getMockPageDataFrom(database, romanBritainCopy1)
  schoolLib.app.books.itemsBorrowed.postSaveNewItemsBorrowed(
    pageData, itemsPhysicalId=1, borrowersId=1
  )

  pageData = getMockPageDataFrom(database, farmAnimalsCopy1)
  schoolLib.app.books.itemsBorrowed.postSaveNewItemsBorrowed(
    pageData, itemsPhysicalId=2, borrowersId=2
  )

