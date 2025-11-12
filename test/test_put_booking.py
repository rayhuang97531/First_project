#測試Booking API - 整筆訂單資料更新
#基礎腳本編寫

import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def create_token():
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth", json=auth_data)
    return response.json()["token"]


def create_booking():
    booking_data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-02"
        },
        "additionalneeds": "Breakfast"
    }
    
    response = requests.post(f"{BASE_URL}/booking", json=booking_data)
    return response.json()["bookingid"]


def test_Update_Bookingvalid_data():
    print("Testing PUT booking with valid data...")
    
    token = create_token()
    print(f"Token: {token}")
    
    booking_id = create_booking()
    print(f"Booking ID: {booking_id}")
    
    updated_booking_data = {
        "firstname": "Kevin",
        "lastname": "Bob",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-10-10",
            "checkout": "2025-10-11"
        },
        "additionalneeds": "Breakfast"
    }
    
    headers = {"Content-Type": "application/json","Cookie": f"token={token}"}
    
    response = requests.put(f"{BASE_URL}/booking/{booking_id}",json=updated_booking_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✓ Test passed!")
    
    data = response.json()
    assert data["firstname"] == "Kevin", "Firstname no match"
    assert data["lastname"] == "Bob", "Lastname no match"
    assert data["totalprice"] == 111, "Total price no match"
    assert data["bookingdates"]["checkin"] == "2025-10-10", "Checkin no match"
    assert data["bookingdates"]["checkout"] == "2025-10-11", "Checkout no match"
    assert data["additionalneeds"] == "Breakfast", "Additional needs no match"
    
    print("✓ Test passed!")


if __name__ == "__main__":
    print("Running PUT booking tests...\n")
    
    test_Update_Bookingvalid_data()
    print()
    
    print("All PUT booking tests completed!")