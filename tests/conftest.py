
import os
# import pytest
import sys

################################################################
# load the test utilities

sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

import tests.utils

from tests.fixtures.database import database
from tests.fixtures.people.classes import addSomeClasses

