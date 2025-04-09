
import pytest

from starlette.testclient import TestClient

from schoolLib.app.main import app

@pytest.mark.skip('not yet')
def test_newBorrower() :
  client = TestClient(app)
  response = client.get('/borrowers/new')
  # assert response.status_code == 200
  print(response.status_code)
  print(response.headers)
  print(response.text)
  # print(getResponseBody(response))
  assert False

@pytest.mark.skip('not yet')
def test_listClasses() :
  client = TestClient(app)
  response = client.get('/classes')
  assert response.status_code == 200
