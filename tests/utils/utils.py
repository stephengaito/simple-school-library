
import yaml

from schoolLib.setup.router import PageData
from schoolLib.setup.authenticate import SLibUser

def getResponseBody(response) :
  return b"\n".join(list(response.stream)).decode('utf-8')

def structureHasKeyValue(aStruc, aKey, aValue) :
  hasKeyValue = False

  if isinstance(aStruc, list) :
    for aSubStruc in aStruc :
      hasKeyValue |= structureHasKeyValue(aSubStruc, aKey, aValue)
    return hasKeyValue

  if isinstance(aStruc, dict) :
    for aStrucKey, aStrucValue in aStruc.items() :
      if aStrucKey == aKey and aStrucValue == aValue :
        return True

      if isinstance(aStrucValue, dict) :
        hasKeyValue |= structureHasKeyValue(aStrucValue, aKey, aValue)
    return hasKeyValue

# NOTES:
#   urlPath is ONLY used by the
#   `schoolLib.setup.router:htmlResponseFromHtmx` method
#   which we do not usually use in our testing.

class MockPageData(PageData) :

  def __init__(
    self, db, urlPath="/", headers={}, theForm={}, authenticated=True
  ) :
    super().__init__(db)
    self.form = theForm
    self.headers = headers
    self.path = urlPath
    if authenticated :
      self.user = SLibUser()

def getMockPageDataFrom(db, pageDictYamlStr) :
  pageDict = {}
  try :
    pageDict = yaml.safe_load(pageDictYamlStr)
  except Exception as err :
    print(repr(err))
  return MockPageData(db, **pageDict)
