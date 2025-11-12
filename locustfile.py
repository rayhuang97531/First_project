#測試Booking API - Locust壓力測試 - 整筆訂單資料更新

import requests
from locust import HttpUser, task, between

class TestRestfulBooker(HttpUser):
    wait_time = between(1,5)

    @task(1)
    def get_all_bookings(self):
        self.client.get("/booking")

    @task(2)
    def post_booking(self):
        headers = {"Content-Type": "application/json"}
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
        response = self.client.post("/booking", json=booking_data , headers=headers)
        return response.json()["bookingid"]

    @task(1)
    def create_token(self):
        auth_data = {
            "username": "admin",
            "password": "password123"
        }
        response = self.client.post("/auth", json=auth_data)
        return response.json()["token"]

    @task(1)
    def put_booking(self):
        
        booking_id = self.post_booking()
        token = self.create_token()
        headers = {"Content-Type": "application/json","Cookie": f"token={token}"}

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
        self.client.put(f"/booking/{booking_id}", json=updated_booking_data , headers=headers)