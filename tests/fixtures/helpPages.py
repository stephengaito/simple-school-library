

import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known items info to the database

helpPage1 = """
authenticated: True
theForm:
  helpContent: This is the help for page 1
"""

helpPage2 = """
authenticated: True
theForm:
  helpContent: This is the help for page 2
"""

@pytest.fixture
def addSomeHelpPages(database) :

  pageData = getMockPageDataFrom(database, helpPage1)
  schoolLib.htmxComponents.helpPages.postHelpPage(
    pageData, "helpPage1", modal=False
  )

  pageData = getMockPageDataFrom(database, helpPage2)
  schoolLib.htmxComponents.helpPages.postHelpPage(
    pageData, "helpPage2", modal=False
  )

