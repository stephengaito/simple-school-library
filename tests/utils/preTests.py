
import os
import sys

sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
  "tests")
)

from tests.utils.sanityChecks import runSanityChecks

from tests.utils.generator import generateTests

if __name__ == '__main__' :
  runSanityChecks()
  generateTests()
