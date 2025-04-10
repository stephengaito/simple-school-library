
import os
# import pytest
import sys

################################################################
# load the test utilities

sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

import tests.utils

from tests.fixtures.database import database
from tests.fixtures.people.classes import addSomeClasses
from tests.fixtures.people.borrowers import addSomeBorrowers
from tests.fixtures.books.itemsInfo import addSomeItemsInfo
from tests.fixtures.books.itemsPhysical import addSomeItemsPhysical

