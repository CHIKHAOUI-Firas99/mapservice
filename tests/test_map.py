from fastapi.testclient import TestClient
from main import app


client = TestClient(app)
map ={
  "name": "w5",
  "mapUrl": "string",
  "objects": [
    {
      "path": "string",
      "x": 0,
      "y": 0,
      "scaleX": 0,
      "scaleY": 0,
      "flipX": True,
      "flipY": True,
      "o": 0,
      "type": "desk"
    },
    {
      "path": "string",
      "x": 0,
      "y": 0,
      "scaleX": 0,
      "scaleY": 0,
      "flipX": True,
      "flipY": True,
      "o": 0,
      "type": "door"
    }
  ]
}
#TEST ADD WORKSPACE
def test_addWorkspace():
    response = client.post('/workspace' , json = map)
    assert response.status_code == 201
    assert response.json() == {"detail" : "Workspace created successfully."}

def test_addWorkspaceUsingExistingName():
    response = client.post('/workspace' , json = map)
    assert response.status_code == 401
    assert response.json() == {"detail" : "name already in use"}