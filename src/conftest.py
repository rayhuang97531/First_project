import pytest
import requests
from src.config import BASE_URL

@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def verify_api_health():
    """Verify API is accessible before running tests."""
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=10)
        if response.status_code != 201:
            pytest.skip("API is not healthy or accessible")
    except requests.exceptions.RequestException:
        pytest.skip("API is not accessible")

@pytest.fixture
def create_token(): #產出Token
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth", json=auth_data)
    assert response.status_code == 200, f"Failed to get auth token: {response.status_code}"
    token = response.json()["token"]
    print("token get")
    yield token
    print("use token")

@pytest.fixture
def create_booking(create_booking_data):   #創建訂房
    print("create booking")
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/booking", json=create_booking_data, headers=headers)
    
    assert response.status_code == 200, f"Failed to create booking: {response.status_code}"
    data = response.json()
    print("create success")
    return {
        "booking_id": data["bookingid"],
        "booking_data": data["booking"]
    }

@pytest.fixture
def create_booking_data():
    return {
        "firstname": "Young",
        "lastname": "Boy",
        "totalprice": 125,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-10-16",
            "checkout": "2025-10-19"
        },
        "additionalneeds": "Breakfast"
    }


