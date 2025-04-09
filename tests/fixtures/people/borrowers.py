
import pytest

import schoolLib
from tests.utils.utils import getMockPageDataFrom

# add some known borrowers to the database

buryCope = """
authenticated: True
theForm:
  firstName: Bury
  familyName: Cope
  cohort: 2025
  assignedClass: 1
"""

charterTrack = """
authenticated: True
theForm:
  firstName: Charter
  familyName: Track
  cohort: 2024
  assignedClass: 2
"""

folkCurtain = """
authenticated: True
theForm:
  firstName: Folk
  familyName: Curtain
  cohort: 2023
  assignedClass: 2
"""

# classId 3 is empty and can be deleted...

someBorrowers = [ buryCope, charterTrack, folkCurtain ]

@pytest.fixture
def addSomeBorrowers(database, addSomeClasses) :
  for aBorrowerYaml in someBorrowers :
    pageData = getMockPageDataFrom(database, aBorrowerYaml)
    schoolLib.app.people.borrowers.postSaveNewBorrower(pageData)

