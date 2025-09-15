#自動測試的網站：PChome
#新增：搜尋功能測試、表單互動測試
import pytest, os, time
from playwright.sync_api import sync_playwright, Page, Browser
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
        self.page = self.browser.new_page()
        
    def teardown_method(self):
        self.page.close()
        print("--- end test ---")
    
    ### Frontend Tests ###
    def test01_pchome_webopen(self):
        print("Testing PChome webpage opening function")
        
        self.page.goto("https://24h.pchome.com.tw/")
        time.sleep(3)
        assert "PChome 24h購物" in self.page.title()
    
    def test02_pchome_search(self):
        self.page.goto("https://24h.pchome.com.tw/")
        self.page.click('[data-gtm-name="close"]')
        search_input = self.page.locator('input[type="search"]')
        #此段AI有建議:是為了避免這個視窗萬一不存在時。教練的建議是?
        #我確實自己在手動測試時有時候會出現有時候不會出現
        '''
        try:
            close_button = self.page.locator('[data-gtm-name="close"]')
        except:
            pass
        '''
        search_input.fill("iPhone17")
        search_input.press("Enter")     
        #不設定會秒關，設定time.sleep(3)出現FAILED:FAILED Lesson11Homework.py::TestPlaywright01::test02_pchome_search - playwright._impl._errors.TimeoutError: Page.wait_for_selector: Timeout 30000ms exceeded.有什麼方法解決?
        self.page.wait_for_selector('h1') 
        results = self.page.locator('h1').count()
        assert results > 0
        assert "iphone17" in self.page.title().lower()
        #title關鍵字還有什麼方式可以斷言比較鬆一點。
    
    def test03_pchome_interaction(self):
        self.page.goto("https://ecvip.pchome.com.tw/login/v3/login.htm?rurl=https%3A%2F%2F24h.pchome.com.tw%2F&mrg=1&_gl=1*14gntc2*_gcl_aw*R0NMLjE3NTc3NzE3ODAuRUFJYUlRb2JDaE1JdmVuemtmTFZqd01WWmRFV0JSMndwd2k3RUFBWUFTQUFFZ0t6QWZEX0J3RQ..*_gcl_au*MTc5OTA1MjEyLjE3NTc3NzE3Nzg.*_ga*MTg5NDMzMzYzNS4xNzU3NzcxNzgw*_ga_9CE1X6J1FG*czE3NTc3NzU4ODckbzIkZzEkdDE3NTc3NzU5NDUkajIkbDAkaDU3MTEyNjI3MA..*_fplc*NkthU0pCU0dFbEpXdWZlUXZ5ZXRObHFTTlRjck9GQkRFU0ZQbkRSZkhnUUoyV0xlZ2JYczIyQ1lpSkFoTG9RZyUyQjElMkI1RTRFV1ZHTE5pUmVwMiUyQmVtOW5FbFc5QkhvYUVnNm16c28yWEIwZ0xNOUcwMWNqJTJGWU90QmJkd1FGSFElM0QlM0Q.")
        self.page.fill('input[id="loginAcc"]',"testuser001@gmail.com")
        self.page.check('input[id="btnRememberAcc"]')
        email_value = self.page.input_value('input[id="loginAcc"]')
        assert email_value == "testuser001@gmail.com"

   
if __name__ == '__main__':
    #pytest.main(["-s", Script + "::TestPlaywright01::test01_pchome_webopen"])
    #pytest.main(["-s", Script + "::TestPlaywright01::test02_pchome_search"])
    pytest.main(["-s", Script + "::TestPlaywright01::test03_pchome_interaction"])