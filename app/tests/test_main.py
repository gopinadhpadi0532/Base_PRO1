from fastapi.testclient import TestClient
from app.main import app  # Import the 'app' instance from your main file

# Create a TestClient instance
client = TestClient(app)

def test_read_main():
    """
    Tests the root endpoint to ensure it returns a successful response and expected JSON.
    """
    response = client.get("/")
    # Assert that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response body is what we expect
    assert response.json() == {"message": "Hello, World"}