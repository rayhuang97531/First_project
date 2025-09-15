#自動測試的網站：PChome
#開啟網頁、驗證網頁Title
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
    
   
if __name__ == '__main__':
    pytest.main(["-s", Script + "::TestPlaywright01::test01_pchome_webopen"])