#測試Booking API - Delete刪除整筆訂單
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

def test_delete_booking_data():
    print("Testing delete booking data...")
    
    token = create_token()
    print(f"Token: {token}")
    
    booking_id = create_booking()
    print(f"Booking ID: {booking_id}")

    headers = {"Content-Type": "application/json","Cookie": f"token={token}"}
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}",headers=headers)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    print("✓ Test passed!")

    check_response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    print(f"Verification Status Code: {check_response.status_code}")
    assert check_response.status_code == 404, "Booking should not exist after deletion"
    print("✓ Verified: Booking no longer exists!")


if __name__ == "__main__":
    print("Running DELETE booking tests...\n")
    
    test_delete_booking_data()
    print()
    
    print("All DELETE booking tests completed!")