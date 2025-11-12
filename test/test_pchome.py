#自動測試的網站：PChome
#網頁進入、搜尋、郵件記住、折價券、購物車加入功能測試
#有使用videos錄像及trace軌跡做紀錄，可方便回放測試過程

import pytest, os, time
from playwright.sync_api import sync_playwright, Page, Browser, expect
Script = os.path.basename(__file__)

class TestPlaywright01:
    ### Set Class ###
    def setup_class(self):
        print("\n*** Start: Playwright Frontend Tests ***")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        
    def teardown_class(self):
        self.browser.close()
        self.playwright.stop()
        print("\n*** End: Playwright Frontend Tests ***")
    
    ### Set Method ###
    def setup_method(self):
        print("\n--- start test ---")
        self.context = self.browser.new_context(record_video_dir="video/") #新增:啟動新context、錄像
        self.page = self.context.new_page()
        self.page.context.tracing.start(screenshots=True, snapshots=True)   #新增軌跡
        
    def teardown_method(self):
        self.context.tracing.stop(path="trace/trace.zip")   #關閉軌跡生成檔案
        self.page.close()
        self.context.close()
        print("--- end test ---")
    
    ### Frontend Tests ###
    #網頁進入測試
    def test01_pchome_webopen(self):
        print("Testing PChome webpage opening function")
        
        self.page.goto("https://24h.pchome.com.tw/")
        time.sleep(3)
        assert "PChome 24h購物" in self.page.title()
    
    #搜尋功能測試
    def test02_pchome_search(self):
        self.page.goto("https://24h.pchome.com.tw/")
        close_button = self.page.get_by_label("close button")  #給變數
        if close_button.is_visible():   #利用變數檢查元素是否存在且可見
            close_button.click()        #確定有再點擊關閉
        search_input = self.page.locator('input[type="search"]')
        search_input.fill("iPhone17")
        search_input.press("Enter")     
        assert "iPhone17" in self.page.url  # 驗證URL是否包含搜尋參數
        assert "iphone17" in self.page.title().lower()
    
    #登入郵件記住功能測試
    def test03_pchome_interaction(self):
        self.page.goto("https://ecvip.pchome.com.tw/login/v3/login.htm?rurl=https%3A%2F%2F24h.pchome.com.tw%2F&mrg=1&_gl=1*14gntc2*_gcl_aw*R0NMLjE3NTc3NzE3ODAuRUFJYUlRb2JDaE1JdmVuemtmTFZqd01WWmRFV0JSMndwd2k3RUFBWUFTQUFFZ0t6QWZEX0J3RQ..*_gcl_au*MTc5OTA1MjEyLjE3NTc3NzE3Nzg.*_ga*MTg5NDMzMzYzNS4xNzU3NzcxNzgw*_ga_9CE1X6J1FG*czE3NTc3NzU4ODckbzIkZzEkdDE3NTc3NzU5NDUkajIkbDAkaDU3MTEyNjI3MA..*_fplc*NkthU0pCU0dFbEpXdWZlUXZ5ZXRObHFTTlRjck9GQkRFU0ZQbkRSZkhnUUoyV0xlZ2JYczIyQ1lpSkFoTG9RZyUyQjElMkI1RTRFV1ZHTE5pUmVwMiUyQmVtOW5FbFc5QkhvYUVnNm16c28yWEIwZ0xNOUcwMWNqJTJGWU90QmJkd1FGSFElM0QlM0Q.")
        self.page.fill('input[id="loginAcc"]',"testuser001@gmail.com")
        self.page.check('input[id="btnRememberAcc"]')
        email_value = self.page.input_value('input[id="loginAcc"]')
        assert email_value == "testuser001@gmail.com"

    #折價券功能測試
    def test04_pchome_coupons(self):
        self.page.goto("https://24h.pchome.com.tw/")
        close_button = self.page.get_by_label("close button") 
        if close_button.is_visible():
            close_button.click()
        self.page.get_by_role("link",name = "看全部").click()
        assert "折價券" in self.page.title().strip() #驗證是否進入顯示標題
    
    def test05_pchome_coupon(self):
        self.page.goto("https://24h.pchome.com.tw/")
        close_button = self.page.get_by_label("close button") 
        if close_button.is_visible():
            close_button.click()
        self.page.get_by_text("查看商品").nth(0).click() #查看首頁你的折價券第1個查看商品
        assert "現折" in self.page.title().strip() #驗證是否進入顯示標題

    #加入購物車功能測試
    def test06_pchome_addtocart(self):
        self.page.goto("https://24h.pchome.com.tw/")
        close_button = self.page.get_by_label("close button") 
        if close_button.is_visible():
            close_button.click()
        self.page.get_by_text("日用").nth(0).click()
        self.page.get_by_text("衛生紙").nth(0).click()
        self.page.get_by_title("平版衛生紙").click()
        self.page.get_by_title("平版衛生紙").nth(3).click()
        self.page.get_by_text("加入購物車").click()
        expect(self.page.locator("text=商品已加入購物車！")).to_be_visible()

        
   
if __name__ == '__main__':
    pytest.main(["-s", Script + "::TestPlaywright01::test01_pchome_webopen"])
    pytest.main(["-s", Script + "::TestPlaywright01::test02_pchome_search"])
    pytest.main(["-s", Script + "::TestPlaywright01::test03_pchome_interaction"])
    pytest.main(["-s", Script + "::TestPlaywright01::test04_pchome_coupons"])
    pytest.main(["-s", Script + "::TestPlaywright01::test05_pchome_coupon"])
    pytest.main(["-s", Script + "::TestPlaywright01::test06_pchome_addtocart"])


    