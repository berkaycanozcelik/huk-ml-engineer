from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    print("Response JSON:", response.json())
    assert response.json() == {"message": "Hello HUK"}
