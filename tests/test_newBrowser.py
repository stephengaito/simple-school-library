
from starlette.testclient import TestClient

from schoolLib.app import app

from utils import *

def test_newBorrower() :
  client = TestClient(app)
  response = client.get('/borrowers/new')
  #assert response.status_code == 200
  print(response.status_code)
  print(response.headers)
  print(response.text)
  #print(getResponseBody(response))
  assert False
