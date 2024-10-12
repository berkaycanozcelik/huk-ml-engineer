from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello HUK"}

#TODO: Work In Process
#First need to finish the /predict EP
def test_predict():
    # Sample input data for the /predict/ endpoint
    sample_input = {
        "text": "I love this product, it’s fantastic!"
    }

    # Sending a POST request to the /predict/ endpoint
    response = client.post("/predict/", json=sample_input)

    assert response.status_code == 200
    # Asserting that the response contains a "prediction" field
    response_json = response.json()
    assert "prediction" in response_json
