
import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known items info to the database

romanBritain = """
authenticated: True
theForm:
  title: Roman Britain
  authors: Hebditch, Felicity
  publisher: Evans
  type: Hardback
  keywords: ;Ancient History;Roman Britain;Romans;
  summary: A book about Roman Britain
  series: Britain Through the Ages
  dewey: '936.4'
  isbn: '9780237516420'
"""

farmAnimals = """
authenticated: True
theForm:
  title: Animals on the Farm
  authors: Morgan, Sally
  publisher: Watts
  type: Hardback
  keywords: ;Animals;Farm Animals;Farms;
  summary: A book about farm animals
  series: Animals That Help Us
  dewey: '632'
  isbn: '9780749633165'
"""

waterSports = """
authenticated: True
theForm:
  title: Water Sports
  authors: McManners, Hugh
  publisher: Dorling Kindersley
  type: Paperback
  keywords: ;Sport;Water Sports;
  summary: A book about water sports
  series: Adventure Handbooks
  dewey: '797'
  isbn: '9780751355024'
"""

someItemsInfo = [ romanBritain, farmAnimals, waterSports ]

@pytest.fixture
def addSomeItemsInfo(database) :
  for anItemInfoYaml in someItemsInfo :
    pageData = getMockPageDataFrom(database, anItemInfoYaml)
    schoolLib.app.books.itemsInfo.postSaveNewItemsInfo(pageData)


