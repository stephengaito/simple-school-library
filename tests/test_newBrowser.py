
import pytest

from starlette.testclient import TestClient

from schoolLib.app.main import app

def test_newBorrower() :
  pytest.skip('not yet')
  client = TestClient(app)
  response = client.get('/borrowers/new')
  # assert response.status_code == 200
  print(response.status_code)
  print(response.headers)
  print(response.text)
  # print(getResponseBody(response))
  assert False

def test_listClasses() :
  pytest.skip('not yet')
  client = TestClient(app)
  response = client.get('/classes')
  assert response.status_code == 200
