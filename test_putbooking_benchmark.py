import requests
import pytest
from config import BASE_URL

class TestAPIBenchmarks:
    def test_benchmark_get_booking(self, benchmark, create_booking):
        booking_id = create_booking["booking_id"]

        result = benchmark(requests.get, f"{BASE_URL}/booking/{booking_id}")

        assert result.status_code == 200

    def test_benchmark_put_booking(self, benchmark, create_token, create_booking):
        booking_id = create_booking["booking_id"]

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
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={create_token}"
        }

        result = benchmark(
            requests.put, f"{BASE_URL}/booking/{booking_id}",
            json = updated_booking_data,
            headers = headers
        )

        assert result.status_code == 200

