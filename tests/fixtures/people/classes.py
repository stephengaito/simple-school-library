
import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known classes to the database

badgers = """
authenticated: True
theForm:
  className: Badgers
  classOrder: 10
  classDesc: The badgers
  classColour: red
"""

squirrels = """
authenticated: True
theForm:
  className: Squirrels
  classOrder: 20
  classDesc: The squirrels
  classColour:  orange
"""

owls = """
authenticated: True
theForm:
  className: Owls
  classOrder: 20
  classDesc: The owls
  classColour:  purple
"""

someClasses = [badgers, squirrels, owls]

@pytest.fixture
def addSomeClasses(database) :
  for aClassYaml in someClasses :
    pageData = getMockPageDataFrom(database, aClassYaml)
    schoolLib.app.people.classes.postSaveNewClass(pageData)
