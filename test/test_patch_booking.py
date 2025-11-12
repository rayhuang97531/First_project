#測試Booking API - 訂單部分資料更新
#運用設定檔config及fixture

import requests
import pytest
from src.config import BASE_URL

class Test_patch_booking:
    def test_patch_booking(self,create_token,create_booking):
        booking_id = create_booking["booking_id"]

        #驗證創建資料
        get_response = requests.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_response.status_code == 200, f"Failed to get booking: {get_response.status_code}"
        initial_data = get_response.json()
        assert initial_data["firstname"] == "Young"
        assert initial_data["lastname"] == "Boy"
        assert initial_data["totalprice"] == 125

        #進行patch測試
        #patch_data資料
        patch_data = {
            "lastname": "Girl",
            "totalprice": 110
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={create_token}"
        }

        patch_response = requests.patch(
            f"{BASE_URL}/booking/{booking_id}",
            json=patch_data,
            headers=headers
        )

        assert patch_response.status_code == 200, f"Expected 200, got {patch_response.status_code}"
        patched_data = patch_response.json()
        #驗證修改的資料
        assert patched_data["lastname"] == "Girl", "Lastname was not updated"
        assert patched_data["totalprice"] == 110, "Total price was not updated"
        #驗證未修改的資料
        assert patched_data["firstname"] == "Young", "Firstname should remain unchanged"
        assert patched_data["depositpaid"] == True, "Depositpaid should remain unchanged"
