
import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known items info to the database

romanBritainCopy1 = """
authenticated: True
theForm:
  barcode: ''
  dateAdded: '2025-03-10'
  dateBorrowed: '2025-03-10'
  dateLastSeen: '2025-03-10'
  status: ''
"""

farmAnimalsCopy1 = """
authenticated: True
theForm:
  barcode: ''
  dateAdded: '2025-03-20'
  dateBorrowed: '2025-03-20'
  dateLastSeen: '2025-03-20'
  status: ''
"""

farmAnimalsCopy2 = """
authenticated: True
theForm:
  barcode: ''
  dateAdded: '2025-03-21'
  dateBorrowed: '2025-03-21'
  dateLastSeen: '2025-03-21'
  status: ''
"""

# There are no copies of water sports

@pytest.fixture
def addSomeItemsPhysical(database) :

  pageData = getMockPageDataFrom(database, romanBritainCopy1)
  schoolLib.app.books.itemsPhysical.postSaveNewItemsPhysical(
    pageData, itemsInfoId=1
  )

  pageData = getMockPageDataFrom(database, farmAnimalsCopy1)
  schoolLib.app.books.itemsPhysical.postSaveNewItemsPhysical(
    pageData, itemsInfoId=2
  )

  pageData = getMockPageDataFrom(database, farmAnimalsCopy2)
  schoolLib.app.books.itemsPhysical.postSaveNewItemsPhysical(
    pageData, itemsInfoId=2
  )

